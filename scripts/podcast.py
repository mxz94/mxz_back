import os
import datetime
import subprocess
import logging
from feedgen.feed import FeedGenerator
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.wavpack import WavPack
from mutagen.ogg import OggFileType
from tqdm import tqdm

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ============== 配置信息 (请修改以下内容) ==============
AUDIO_ROOT_DIR = r"E:\水浒系列"
PODCAST_TITLE = "水浒系列"
PODCAST_AUTHOR = "郭德纲"
PODCAST_DESCRIPTION=PODCAST_TITLE
# 您的服务器域名，所有播客链接的前缀 (使用 HTTPS 是最佳实践)
BASE_URL = f"https://malanxi.top/podcast_files/{PODCAST_TITLE}/"

# 存放播客音频文件的根目录 (脚本将递归扫描此目录及其子文件夹)
# 假设这个脚本在你想要扫描的目录的上一级
# 如果脚本和音频文件在同一个目录下，可以使用 "."


# 输出的 RSS 文件名 (将放置在 AUDIO_ROOT_DIR 目录下)
OUTPUT_FILE = "podcast.xml"

# 播客整体信息
PODCAST_EMAIL = "your-email@example.com"
# 播客封面图片 URL (必须是 JPEG 或 PNG 格式，建议尺寸 1400x1400 到 3000x3000)
PODCAST_IMAGE_URL = BASE_URL + "cover.jpg"
PODCAST_CATEGORY = "Literature"
PODCAST_SUB_CATEGORY = "Books"

# 允许的音频文件扩展名
ALLOWED_EXTENSIONS = ('.mp3', '.m4a', '.mp4')
CONVERT_EXTENSIONS = ('.wma', '.flac', '.ogg', '.wav') # 需要转码的格式

# =======================================================

def get_audio_duration(file_path):
    """使用 mutagen 尝试获取音频时长和文件大小。"""
    try:
        if file_path.lower().endswith('.mp3'):
            audio = MP3(file_path)
        elif file_path.lower().endswith(('.m4a', '.mp4')):
            audio = MP4(file_path)
        # 您可以根据需要添加更多格式支持
        else:
            # 对于其他格式，如果 mutagen 不支持，可以尝试使用 ffprobe (更复杂，这里简化)
            logging.warning(f"未知或不受支持的格式：{file_path}。跳过元数据读取。")
            return None, None

        duration = int(audio.info.length)
        size = os.path.getsize(file_path)
        return duration, size

    except Exception as e:
        logging.error(f"无法读取文件 {file_path} 的元数据: {e}")
        return None, None

def convert_to_mp3(wma_path):
    """使用 FFmpeg 将 WMA 转换为 MP3，并在成功后删除原文件。"""
    # 新文件路径：替换扩展名
    mp3_path = os.path.splitext(wma_path)[0] + '.mp3'

    if os.path.exists(mp3_path):
        logging.info(f"MP3 文件已存在，跳过转码: {mp3_path}")
        return mp3_path

    logging.info(f"正在转码: {wma_path} -> {mp3_path}")

    # FFmpeg 命令：-i 输入 -vn 不包含视频 -acodec libmp3lame 使用高质量MP3编码 -q:a 2 编码质量（0-9, 0最好）
    command = [
        'ffmpeg',
        '-i', wma_path,
        '-vn',
        '-acodec', 'libmp3lame',
        # --- 【修改点】将质量等级从 2 更改为 4 ---
        '-q:a', '4',
        # ----------------------------------------
        mp3_path
    ]

    try:
        # 执行命令，隐藏输出
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 成功转码后，删除原文件
        os.remove(wma_path)
        logging.info(f"✅ 转码成功并删除原文件: {wma_path}")
        return mp3_path
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ FFmpeg 转码失败: {wma_path}. 错误: {e}")
        return None
    except FileNotFoundError:
        logging.error("❌ FFmpeg 未安装或不在系统 PATH 中。请先安装 FFmpeg。")
        return None


def generate_podcast_feed():
    """递归扫描目录、转码并生成播客 RSS 订阅源文件。"""

    logging.info("--- 播客 RSS 自动生成脚本开始 ---")

    # 1. 扫描文件并进行转码
    all_files_to_process = []

    # 递归遍历目录
    for root, _, files in os.walk(AUDIO_ROOT_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            if ext in CONVERT_EXTENSIONS:
                # 发现需要转码的文件，立即转码
                mp3_path = convert_to_mp3(file_path)
                if mp3_path:
                    # 将转码后的 MP3 文件加入列表
                    all_files_to_process.append(mp3_path)

            elif ext in ALLOWED_EXTENSIONS:
                # 发现支持的音频文件
                all_files_to_process.append(file_path)

    # 2. 排序文件
    # 按照文件名进行自然顺序排序（Python 的 sorted 默认行为）
    all_files_to_process = sorted(all_files_to_process)

    if not all_files_to_process:
        logging.warning("未找到任何音频文件（MP3/M4A）或可转码文件。")
        return

    logging.info(f"找到 {len(all_files_to_process)} 个文件准备生成 RSS。")

    # 3. 生成 RSS Feed
    fg = FeedGenerator()
    fg.load_extension('podcast')

    # 设置频道/播客整体信息
    fg.id(BASE_URL)
    fg.title(PODCAST_TITLE)
    fg.author({'name': PODCAST_AUTHOR, 'email': PODCAST_EMAIL})
    fg.link(href=BASE_URL, rel='alternate')
    fg.logo(PODCAST_IMAGE_URL)
    fg.subtitle(PODCAST_DESCRIPTION)
    fg.description(PODCAST_DESCRIPTION)
    fg.language('zh-CN')
    fg.pubDate(datetime.datetime.now(datetime.timezone.utc).astimezone())
    fg.podcast.itunes_image(PODCAST_IMAGE_URL)
    fg.podcast.itunes_category(PODCAST_CATEGORY, PODCAST_SUB_CATEGORY)
    fg.podcast.itunes_explicit('no')
    fg.podcast.itunes_owner(name=PODCAST_AUTHOR, email=PODCAST_EMAIL)


    # 4. 遍历文件并添加单集
    # 使用 tqdm 进度条
    for local_path in tqdm(all_files_to_process, desc="生成 RSS 条目"):

        # 确保路径是相对路径，用于构造 URL
        relative_path = os.path.relpath(local_path, AUDIO_ROOT_DIR).replace('\\', '/')

        # 构造公开访问的 URL
        file_url = BASE_URL + relative_path

        # 获取文件元数据
        duration_seconds, file_size_bytes = get_audio_duration(local_path)

        if duration_seconds is None or file_size_bytes is None:
            logging.error(f"跳过文件 {relative_path}，无法获取元数据。")
            continue

        # 使用文件名（去除后缀）作为标题
        episode_title = os.path.splitext(os.path.basename(local_path))[0]

        # 为每集使用不同的发布时间，确保客户端能按顺序识别
        pub_date = datetime.datetime.now(datetime.timezone.utc).astimezone()

        fe = fg.add_entry()
        fe.id(file_url)
        fe.title(episode_title)
        fe.description(f"集数: {episode_title}")
        fe.published(pub_date)

        # 核心：设置音频附件
        # 核心：设置音频附件
        fe.enclosure(url=file_url, length=str(file_size_bytes), type='audio/mpeg')

        # --- 【最终修正】使用标准的 <guid> 标签，并移除不支持的 isPermaLink 参数 ---
        fe.guid(relative_path)

        # iTunes 标签
        fe.podcast.itunes_duration(duration_seconds)
        fe.podcast.itunes_author(PODCAST_AUTHOR)

    # 5. 生成并保存 XML 文件
    output_path = os.path.join(AUDIO_ROOT_DIR, OUTPUT_FILE)
    try:
        fg.rss_file(output_path, pretty=True)
        logging.info(f"\n✅ RSS 订阅源已成功生成到文件: {output_path}")
        logging.info(f"✅ 您的播客 RSS URL 为: {BASE_URL}{OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"\n❌ 生成文件时出错: {e}")

def generate_player_html():
    """生成播客 HTML 播放器页面。"""
    rss_url_public = BASE_URL + OUTPUT_FILE
    # 构造本地输出路径
    html_output_path = os.path.join(AUDIO_ROOT_DIR, 'index.html')

    logging.info("--- 静态播放器 HTML 生成脚本开始 ---")

    # 传递封面URL和作者名
    generate_player_html_new(rss_url_public, OUTPUT_FILE, PODCAST_AUTHOR, PODCAST_IMAGE_URL, html_output_path)

def generate_player_html_new(rss_url, podcast_title, podcast_author, cover_url, html_output_path):
    """
    生成包含 JavaScript 播放器的静态 index.html 文件。
    - V4: 怀旧复古风格 + 每个剧集独立播放器和自定义进度条
    - 保持剧集倒序(最新在上)。
    - 记录每个剧集的播放进度。
    - 播放互斥:播放某个剧集时自动暂停其他剧集。
    """

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{podcast_title} | 在线播客</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Courier+Prime&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-bg: #e8dcc4;
            --card-bg: #f5ead6;
            --text-main: #3d2817;
            --text-muted: #8b6f47;
            --accent-color: #a0522d;
            --accent-warm: #cd853f;
            --playing-bg: #fef5e7;
            --shadow-vintage: 0 4px 8px rgba(61, 40, 23, 0.2);
            --border-vintage: #8b6f47;
            --radius-vintage: 4px;
        }}

        body {{ 
            font-family: 'Noto Serif SC', Georgia, serif;
            background: #e8dcc4;
            background-image: 
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139, 111, 71, 0.03) 2px, rgba(139, 111, 71, 0.03) 4px),
                repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(139, 111, 71, 0.03) 2px, rgba(139, 111, 71, 0.03) 4px);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            line-height: 1.8;
            position: relative;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" /></filter><rect width="100" height="100" filter="url(%23noise)" opacity="0.05"/></svg>');
            pointer-events: none;
            z-index: 1;
        }}
        
        .main-container {{
            position: relative;
            z-index: 2;
            max-width: 900px; 
            margin: 30px auto; 
        }}

        .header-hero {{
            background: linear-gradient(to bottom, #d4b896 0%, #c9a978 100%);
            border: 3px solid var(--border-vintage);
            border-radius: var(--radius-vintage);
            padding: 40px;
            display: flex;
            align-items: center;
            box-shadow: 
                var(--shadow-vintage),
                inset 0 1px 0 rgba(255, 255, 255, 0.3),
                inset 0 -1px 0 rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }}
        
        .header-hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(139, 111, 71, 0.02) 10px, rgba(139, 111, 71, 0.02) 20px);
            pointer-events: none;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            z-index: 2;
        }}

        .cover-image-large {{
            width: 160px;
            height: 160px;
            min-width: 160px;
            background-image: url('{cover_url}');
            background-size: cover;
            background-position: center;
            border-radius: var(--radius-vintage);
            margin-right: 35px;
            box-shadow: 0 0 0 4px #8b6f47, 0 0 0 8px #f5ead6, var(--shadow-vintage);
            border: 2px solid #3d2817;
            filter: sepia(0.2) contrast(1.1);
        }}
        
        .title-info h1 {{
            margin: 0;
            color: var(--text-main);
            font-size: 2.4em;
            font-weight: 700;
            letter-spacing: 1px;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
        }}
        
        .title-info .author {{
            margin: 10px 0 0 0;
            font-size: 1.1em;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            font-family: 'Courier Prime', monospace;
        }}
        
        .title-info .author i {{
            margin-right: 8px;
            color: var(--accent-color);
        }}

        .list-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding: 0 10px;
        }}
        .list-header h2 {{
            margin: 0;
            font-size: 1.5em;
            font-weight: 600;
            color: var(--text-main);
            letter-spacing: 1px;
        }}
        
        #loading-message {{
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 1.2em;
        }}

        .episode-list {{ list-style: none; padding: 0; margin: 0; }}
        
        .episode-item {{ 
            padding: 20px; 
            margin-bottom: 15px;
            background: var(--card-bg); 
            border-radius: var(--radius-vintage);
            box-shadow: var(--shadow-vintage);
            border: 2px solid var(--border-vintage);
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .episode-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(90deg, transparent, transparent 1px, rgba(139, 111, 71, 0.02) 1px, rgba(139, 111, 71, 0.02) 2px);
            pointer-events: none;
        }}
        
        .episode-item:hover {{ 
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(61, 40, 23, 0.25);
            border-color: var(--accent-color);
        }}
        
        .episode-item.playing {{
            background-color: var(--playing-bg);
            border-color: var(--accent-color);
            border-width: 3px;
        }}
        .episode-item.playing::after {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 6px;
            background: var(--accent-color);
        }}

        .episode-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }}

        .episode-info {{ text-align: left; flex-grow: 1; margin-right: 20px; }}
        
        .episode-title {{ 
            font-weight: 600; 
            font-size: 1.15em; 
            color: var(--text-main); 
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}
        .episode-item.playing .episode-title {{ 
            color: var(--accent-color);
            font-weight: 700;
        }}
        
        .episode-date {{ 
            font-size: 0.9em; 
            color: var(--text-muted); 
            display: flex;
            align-items: center;
            font-family: 'Courier Prime', monospace;
        }}
        .episode-date i {{ margin-right: 6px; font-size: 0.9em; }}

        .play-button-wrapper {{
            position: relative;
            width: 60px;
            height: 60px;
            flex-shrink: 0;
        }}
        
        .play-button {{ 
            background: linear-gradient(to bottom, #8b6f47 0%, #6b5637 50%, #5a4527 100%);
            color: #f5ead6; 
            border: 3px solid #3d2817;
            width: 100%;
            height: 100%;
            border-radius: var(--radius-vintage);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4em;
            box-shadow: 0 4px 0 #3d2817, 0 6px 8px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
            cursor: pointer;
            position: relative;
        }}
        
        .play-button:active {{ 
            transform: translateY(3px);
            box-shadow: 0 1px 0 #3d2817, 0 2px 4px rgba(0, 0, 0, 0.3), inset 0 1px 2px rgba(0, 0, 0, 0.3);
        }}
        
        .episode-item.playing .play-button {{
            background: linear-gradient(to bottom, #cd853f 0%, #a0522d 50%, #8b4513 100%);
            border-radius: 50%;
            border-color: #5a3410;
            box-shadow: 0 4px 0 #5a3410, 0 6px 8px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3), 0 0 0 3px rgba(205, 133, 63, 0.3);
        }}
        
        .episode-item.playing .play-button:active {{
            box-shadow: 0 1px 0 #5a3410, 0 2px 4px rgba(0, 0, 0, 0.3), inset 0 1px 2px rgba(0, 0, 0, 0.3), 0 0 0 3px rgba(205, 133, 63, 0.3);
        }}
        
        .play-button:hover:not(:active) {{ filter: brightness(1.1); }}

        /* 嵌入式播放器样式 */
        .episode-player {{
            background: linear-gradient(to bottom, #c9a978, #b89968);
            padding: 15px;
            border: 2px solid var(--border-vintage);
            border-radius: var(--radius-vintage);
            margin-top: 15px;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
            position: relative;
        }}

        .episode-player::before {{
            content: '';
            position: absolute;
            top: 6px;
            left: 6px;
            right: 6px;
            bottom: 6px;
            border: 1px solid rgba(61, 40, 23, 0.2);
            border-radius: 2px;
            pointer-events: none;
        }}

        .episode-audio {{
            display: none;
        }}

        /* 自定义进度条 */
        .custom-controls {{
            position: relative;
            z-index: 2;
        }}

        .progress-bar-container {{
            width: 100%;
            height: 10px;
            background: rgba(61, 40, 23, 0.3);
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 10px;
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 2px 3px rgba(0, 0, 0, 0.3);
        }}

        .progress-bar {{
            height: 100%;
            background: linear-gradient(to right, var(--accent-color), var(--accent-warm));
            border-radius: 5px;
            width: 0%;
            transition: width 0.1s linear;
            position: relative;
        }}

        .progress-bar::after {{
            content: '';
            position: absolute;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 14px;
            height: 14px;
            background: var(--accent-warm);
            border: 2px solid #3d2817;
            border-radius: 50%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .time-display {{
            display: flex;
            justify-content: space-between;
            font-family: 'Courier Prime', monospace;
            font-size: 0.85em;
            color: #3d2817;
            font-weight: 600;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid var(--border-vintage);
            font-size: 0.9em;
            color: var(--text-muted);
        }}
        .footer a {{ 
            color: var(--accent-color); 
            text-decoration: none;
            font-weight: 600;
        }}
        .footer a:hover {{ text-decoration: underline; }}

        @media (max-width: 768px) {{
            body {{ padding: 15px; }}
            .header-hero {{ flex-direction: column; text-align: center; padding: 30px 20px; }}
            .header-content {{ flex-direction: column; }}
            .cover-image-large {{ margin-right: 0; margin-bottom: 20px; width: 140px; height: 140px; min-width: 140px; }}
            .title-info h1 {{ font-size: 1.8em; }}
            .title-info .author {{ justify-content: center; }}
            .episode-item {{ padding: 15px; }}
            .play-button-wrapper {{ width: 52px; height: 52px; }}
            .play-button {{ font-size: 1.2em; }}
        }}
    </style>
</head>
<body>

<div class="main-container">
    <div class="header-hero">
        <div class="header-content">
            <div class="cover-image-large"></div>
            <div class="title-info">
                <h1>{podcast_title}</h1>
                <div class="author">
                    <i class="fas fa-microphone-alt"></i>
                    <span>主理人:{podcast_author}</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="list-header">
        <h2>节目列表</h2>
    </div>

    <div id="loading-message">
        <i class="fas fa-spinner fa-spin"></i> 正在获取节目单...
    </div>
    
    <ul id="episode-list" class="episode-list"></ul>
    
    <div class="footer">
        <p>
            源数据基于 RSS 订阅源 <a href="{rss_url}" target="_blank">Feed Link</a>
            | 自托管播客系统
        </p>
    </div>
</div>

<script>
    const RSS_FEED_URL = '{rss_url}';
    const EPISODE_LIST = document.getElementById('episode-list');
    const LOADING_MESSAGE = document.getElementById('loading-message');
    const STORAGE_KEY = 'podcast_episodes_progress_v4';
    
    let allAudioPlayers = [];

    function formatTime(seconds) {{
        if (isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
    }}

    function loadAllProgress() {{
        const stored = localStorage.getItem(STORAGE_KEY);
        return stored ? JSON.parse(stored) : {{}};
    }}

    function saveEpisodeProgress(audioUrl, currentTime, duration) {{
        const allProgress = loadAllProgress();
        
        if (currentTime > 5 && currentTime < duration - 10) {{
            allProgress[audioUrl] = {{
                time: currentTime,
                duration: duration,
                timestamp: Date.now()
            }};
        }} else if (currentTime >= duration - 10) {{
            delete allProgress[audioUrl];
        }}
        
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allProgress));
    }}

    function getEpisodeProgress(audioUrl) {{
        const allProgress = loadAllProgress();
        return allProgress[audioUrl] || null;
    }}

    function pauseOtherPlayers(currentAudio) {{
        allAudioPlayers.forEach(audio => {{
            if (audio !== currentAudio && !audio.paused) {{
                audio.pause();
            }}
        }});
    }}

    function updatePlayingUI() {{
        document.querySelectorAll('.episode-item').forEach(item => {{
            const audio = item.querySelector('.episode-audio');
            const button = item.querySelector('.play-button');
            const icon = button.querySelector('i');
            
            if (audio && !audio.paused) {{
                item.classList.add('playing');
                icon.className = 'fas fa-pause';
            }} else {{
                item.classList.remove('playing');
                icon.className = 'fas fa-play';
            }}
        }});
    }}

    function fetchAndParseRSS() {{
        fetch(RSS_FEED_URL)
            .then(response => {{
                if (!response.ok) throw new Error(response.statusText);
                return response.text();
            }})
            .then(str => {{
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(str, "text/xml");
                displayEpisodes(xmlDoc);
            }})
            .catch(error => {{
                console.error("Error:", error);
                LOADING_MESSAGE.innerHTML = `<i class="fas fa-exclamation-circle"></i> 加载失败。<br><small>请检查跨域(CORS)配置或网络。</small>`;
                LOADING_MESSAGE.style.color = '#e74c3c';
            }});
    }}

    function displayEpisodes(xmlDoc) {{
        LOADING_MESSAGE.style.display = 'none';
        const items = xmlDoc.querySelectorAll('item');
        
        if (items.length === 0) {{
             EPISODE_LIST.innerHTML = '<li style="text-align:center;padding:20px;">暂无节目</li>';
             return;
        }}
        
        const reversedItems = Array.from(items).reverse();

        reversedItems.forEach((item, index) => {{
            const title = item.querySelector('title')?.textContent || `第 ${{index + 1}} 集`;
            let pubDateStr = item.querySelector('pubDate')?.textContent;
            let formattedDate = '暂无日期';
            if (pubDateStr) {{
                try {{ formattedDate = new Date(pubDateStr).toLocaleDateString('zh-CN'); }} catch(e) {{}}
            }}
            
            const enclosure = item.querySelector('enclosure');
            const audioUrl = enclosure ? enclosure.getAttribute('url') : null;
            if (!audioUrl) return; 

            const listItem = document.createElement('li');
            listItem.className = 'episode-item';
            
            const progress = getEpisodeProgress(audioUrl);
            const progressIndicator = progress ? ' <span style="color: var(--accent-color); font-weight: 600;">• 继续播放</span>' : '';
            
            listItem.innerHTML = `
                <div class="episode-header">
                    <div class="episode-info">
                        <div class="episode-title">${{title}}</div>
                        <div class="episode-date">
                            <i class="far fa-calendar-alt"></i> ${{formattedDate}}${{progressIndicator}}
                        </div>
                    </div>
                    <div class="play-button-wrapper">
                        <button class="play-button" title="播放/暂停">
                            <i class="fas fa-play"></i>
                        </button>
                    </div>
                </div>
                <div class="episode-player">
                    <audio class="episode-audio" preload="metadata" data-url="${{audioUrl}}">
                        <source src="${{audioUrl}}" type="audio/mpeg">
                    </audio>
                    <div class="custom-controls">
                        <div class="progress-bar-container">
                            <div class="progress-bar" style="width: 0%"></div>
                        </div>
                        <div class="time-display">
                            <span class="current-time">0:00</span>
                            <span class="duration">0:00</span>
                        </div>
                    </div>
                </div>
            `;
            
            const audio = listItem.querySelector('.episode-audio');
            const button = listItem.querySelector('.play-button');
            const progressBar = listItem.querySelector('.progress-bar');
            const progressContainer = listItem.querySelector('.progress-bar-container');
            const currentTimeEl = listItem.querySelector('.current-time');
            const durationEl = listItem.querySelector('.duration');
            
            allAudioPlayers.push(audio);

            // 恢复播放进度
            if (progress && progress.time) {{
                audio.addEventListener('loadedmetadata', () => {{
                    audio.currentTime = progress.time;
                    progressBar.style.width = `${{(progress.time / audio.duration) * 100}}%`;
                    currentTimeEl.textContent = formatTime(progress.time);
                }}, {{ once: true }});
            }}

            // 元数据加载完成后更新总时长
            audio.addEventListener('loadedmetadata', () => {{
                durationEl.textContent = formatTime(audio.duration);
            }});

            // 播放/暂停按钮
            button.addEventListener('click', (e) => {{
                e.stopPropagation();
                if (audio.paused) {{
                    pauseOtherPlayers(audio);
                    audio.play().catch(err => console.warn('播放失败:', err));
                }} else {{
                    audio.pause();
                }}
            }});

            // 进度条更新
            audio.addEventListener('timeupdate', () => {{
                if (audio.duration) {{
                    const percent = (audio.currentTime / audio.duration) * 100;
                    progressBar.style.width = `${{percent}}%`;
                    currentTimeEl.textContent = formatTime(audio.currentTime);
                    
                    // 每10秒保存一次进度
                    if (!audio.paused && audio.currentTime % 10 < 0.5) {{
                        saveEpisodeProgress(audioUrl, audio.currentTime, audio.duration);
                    }}
                }}
            }});

            // 进度条拖动
            progressContainer.addEventListener('click', (e) => {{
                if (audio.duration) {{
                    const rect = progressContainer.getBoundingClientRect();
                    const percent = (e.clientX - rect.left) / rect.width;
                    audio.currentTime = percent * audio.duration;
                }}
            }});

            audio.addEventListener('play', () => {{
                pauseOtherPlayers(audio);
                updatePlayingUI();
            }});

            audio.addEventListener('pause', () => {{
                updatePlayingUI();
                saveEpisodeProgress(audioUrl, audio.currentTime, audio.duration);
            }});

            audio.addEventListener('ended', () => {{
                updatePlayingUI();
                saveEpisodeProgress(audioUrl, audio.currentTime, audio.duration);
            }});

            EPISODE_LIST.appendChild(listItem);
        }});
    }}

    window.addEventListener('beforeunload', () => {{
        allAudioPlayers.forEach(audio => {{
            if (audio.src && !audio.paused) {{
                const url = audio.dataset.url;
                saveEpisodeProgress(url, audio.currentTime, audio.duration);
            }}
        }});
    }});

    fetchAndParseRSS();

</script>
</body>
</html>
"""
    try:
        os.makedirs(os.path.dirname(html_output_path), exist_ok=True)
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logging.info(f"\n✅ **怀旧复古版 HTML (独立播放器+自定义进度条)** 已成功生成: {html_output_path}")
        logging.info(f"请上传至服务器,访问 URL: {rss_url.replace(OUTPUT_FILE, 'index.html')}")
    except Exception as e:
        logging.error(f"❌ 生成 HTML 文件时出错: {e}")

if __name__ == '__main__':
    generate_podcast_feed()
    generate_player_html()
