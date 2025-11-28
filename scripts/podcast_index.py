import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_player_html_new(rss_url, podcast_title, podcast_author, cover_url, html_output_path):
    """
    生成包含 JavaScript 播放器的静态 index.html 文件。
    - V8: 优化性能（按需加载）并增加播放加载状态反馈。
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
            box-shadow: 0 1px 0 #5a3410, 0 2px 4px rgba(0, 0, 0, 0.3), 0 0 0 3px rgba(205, 133, 63, 0.3);
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
        
        /* Season Tabs Style */
        #season-tabs {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
            padding: 0 10px;
        }}
        .season-button {{
            padding: 8px 15px;
            background-color: var(--card-bg);
            color: var(--text-main);
            border: 2px solid var(--border-vintage);
            border-radius: var(--radius-vintage);
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.2s;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .season-button:hover {{
            background-color: #e0d5be;
            border-color: var(--accent-color);
        }}
        .season-button.active {{
            background-color: var(--accent-color);
            color: #f5ead6;
            border-color: #5a4527;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
        }}

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
    
    <div id="season-tabs">
        <div id="loading-tabs">
            <i class="fas fa-sync-alt fa-spin"></i> 正在加载季信息...
        </div>
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
    const LOADING_TABS_MESSAGE = document.getElementById('loading-tabs');
    const SEASON_TABS_CONTAINER = document.getElementById('season-tabs');
    const ITUNES_NS_URI = 'http://www.itunes.com/dtds/podcast-1.0.dtd'; 
    
    // 【V8 存储优化】
    const CURRENT_STORAGE_VERSION = 8;
    const STORAGE_KEY = 'podcast_episodes_progress';
    
    let allAudioPlayers = [];
    let episodesBySeason = {{}}; 
    let currentSeasonId = null;

    function formatTime(seconds) {{
        if (isNaN(seconds) || seconds < 0) return '0:00';
        seconds = parseInt(seconds);
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
    }}

    function loadAllProgress() {{
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {{
            try {{
                const data = JSON.parse(stored);
                // 检查版本号
                if (data.version === CURRENT_STORAGE_VERSION) {{
                    return data.progress || {{}};
                }}
            }} catch (e) {{
                console.error("Error parsing storage data:", e);
            }}
        }}
        // 如果没有存储、存储过期或版本不匹配，返回空对象
        return {{}};
    }}

    function saveEpisodeProgress(audioUrl, currentTime, duration) {{
        const allProgress = loadAllProgress(); // 获取当前进度的副本
        
        if (currentTime > 5 && duration && currentTime < duration - 10) {{
            allProgress[audioUrl] = {{
                time: currentTime,
                duration: duration,
                timestamp: Date.now()
            }};
        }} else if (duration && currentTime >= duration - 10) {{
            // 接近结束，清除进度
            delete allProgress[audioUrl];
        }}
        
        // 最终存储时，带上版本号
        const dataToStore = {{ 
            version: CURRENT_STORAGE_VERSION, 
            progress: allProgress 
        }};
        localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToStore));
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
            
            if (audio) {{
                const button = item.querySelector('.play-button');
                const icon = button.querySelector('i');
                
                if (!audio.paused) {{
                    item.classList.add('playing');
                    // 播放中或缓冲中，显示暂停图标
                    if (!icon.classList.contains('fa-spinner')) {{
                        icon.className = 'fas fa-pause';
                    }}
                }} else {{
                    item.classList.remove('playing');
                    // 非播放中，恢复播放图标，除非显示错误
                    if (!icon.classList.contains('fa-spinner') && !icon.classList.contains('fa-exclamation-triangle')) {{
                        icon.className = 'fas fa-play';
                    }}
                }}
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
                groupEpisodesBySeason(xmlDoc);
            }})
            .catch(error => {{
                console.error("Error fetching or parsing RSS:", error);
                LOADING_MESSAGE.innerHTML = `<i class="fas fa-exclamation-circle"></i> 加载失败。请检查 RSS 文件或 CORS 配置。`;
                LOADING_MESSAGE.style.color = '#e74c3c';
            }});
    }}

    function groupEpisodesBySeason(xmlDoc) {{
        LOADING_MESSAGE.style.display = 'none';
        LOADING_TABS_MESSAGE.style.display = 'none';
        
        const items = xmlDoc.querySelectorAll('item');
        
        if (items.length === 0) {{
             EPISODE_LIST.innerHTML = '<li style="text-align:center;padding:20px;">暂无节目</li>';
             return;
        }}
        
        const sequentialItems = Array.from(items); 

        sequentialItems.forEach(item => {{
            const seasonTags = item.getElementsByTagNameNS(ITUNES_NS_URI, 'subtitle');
            const seasonId = (seasonTags.length > 0) ? seasonTags[0].textContent.trim() : 'Season 1'; 
            
            if (!episodesBySeason[seasonId]) {{
                episodesBySeason[seasonId] = [];
            }}
            
            episodesBySeason[seasonId].push(item);
        }});
        
        renderSeasonTabs(); 
    }}
    
    function renderSeasonTabs() {{
        // 尝试按 Season ID 的数字部分进行正序排序 (S1, S2, S3)
        const seasonIds = Object.keys(episodesBySeason).sort((a, b) => {{
            const numA = parseInt(a.replace(/[^0-9]/g, '')); 
            const numB = parseInt(b.replace(/[^0-9]/g, ''));
            if (!isNaN(numA) && !isNaN(numB)) {{
                return numA - numB; 
            }}
            return a.localeCompare(b); 
        }});
        
        if (seasonIds.length <= 1) {{
             SEASON_TABS_CONTAINER.style.display = 'none';
             if(seasonIds.length > 0) showSeason(seasonIds[0]);
             return;
        }}
        
        SEASON_TABS_CONTAINER.innerHTML = '';
        currentSeasonId = seasonIds[0]; 
        
        seasonIds.forEach(id => {{
            const button = document.createElement('button');
            button.className = 'season-button';
            button.textContent = `${{id}} (${{episodesBySeason[id].length}}集)`;
            button.dataset.seasonId = id;
            
            if (id === currentSeasonId) {{
                button.classList.add('active');
            }}
            
            button.addEventListener('click', () => showSeason(id));
            SEASON_TABS_CONTAINER.appendChild(button);
        }});
        
        showSeason(currentSeasonId);
    }}
    
function showSeason(seasonId) {{
        currentSeasonId = seasonId;
        EPISODE_LIST.innerHTML = ''; 
        allAudioPlayers = []; 
        
        // 激活当前 Season Tab
        document.querySelectorAll('.season-button').forEach(btn => {{
            btn.classList.remove('active');
            if (btn.dataset.seasonId === seasonId) {{
                btn.classList.add('active');
            }}
        }});
        
        const seasonEpisodes = episodesBySeason[seasonId];
        if (!seasonEpisodes) return;
        
        seasonEpisodes.forEach((item, index) => {{
            const title = item.querySelector('title')?.textContent || `第 ${{index + 1}} 集`;
            let pubDateStr = item.querySelector('pubDate')?.textContent;
            let formattedDate = '暂无日期';
            if (pubDateStr) {{
                try {{ formattedDate = new Date(pubDateStr).toLocaleDateString('zh-CN'); }} catch(e) {{}}
            }}
            
            const enclosure = item.querySelector('enclosure');
            const audioUrl = enclosure ? enclosure.getAttribute('url') : null;
            if (!audioUrl) return; 
            
            const durationTags = item.getElementsByTagNameNS(ITUNES_NS_URI, 'duration');
            const durationSeconds = (durationTags.length > 0) ? parseInt(durationTags[0].textContent.trim()) : 0;
            
            const listItem = document.createElement('li');
            listItem.className = 'episode-item';
            
            const progress = getEpisodeProgress(audioUrl);
            const initialTime = progress ? progress.time : 0;
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
                    <audio class="episode-audio" preload="none" 
                           data-audio-url="${{audioUrl}}" 
                           data-duration="${{durationSeconds}}" 
                           data-initial-time="${{initialTime}}">
                    </audio>
                    <div class="custom-controls">
                        <div class="progress-bar-container">
                            <div class="progress-bar" style="width: ${{durationSeconds > 0 ? (initialTime / durationSeconds) * 100 : 0}}%"></div>
                        </div>
                        <div class="time-display">
                            <span class="current-time">${{formatTime(initialTime)}}</span>
                            <span class="duration">${{formatTime(durationSeconds)}}</span>
                        </div>
                    </div>
                </div>
            `;
            
            const audio = listItem.querySelector('.episode-audio');
            const button = listItem.querySelector('.play-button');
            const progressBar = listItem.querySelector('.progress-bar');
            const progressContainer = listItem.querySelector('.progress-bar-container');
            const currentTimeEl = listItem.querySelector('.current-time');
            
            allAudioPlayers.push(audio);
            
            const duration = parseFloat(audio.dataset.duration);
            const initialTimeValue = parseFloat(audio.dataset.initialTime);
            
            // =========================================================
            // 【V8 核心逻辑：按需加载与加载状态反馈】
            // =========================================================
            const loadAndPlay = () => {{
                const icon = button.querySelector('i');

                // 1. 如果音频源未设置，则设置它并强制加载
                if (!audio.src) {{
                    audio.src = audio.dataset.audioUrl;
                    audio.load();
                }}

                // 2. 显示加载图标
                if (audio.paused) {{
                    icon.className = 'fas fa-spinner fa-spin'; 
                }}

                // 3. 监听 readyState 变化，在可以播放时移除加载图标
                const removeLoading = () => {{
                    // 确保播放成功后才移除加载图标并更新UI
                    if (!audio.paused) {{
                         icon.className = 'fas fa-pause';
                         updatePlayingUI();
                    }}
                    audio.removeEventListener('playing', removeLoading);
                    audio.removeEventListener('canplay', removeLoading);
                }};

                audio.addEventListener('playing', removeLoading);
                audio.addEventListener('canplay', removeLoading); 

                // 4. 恢复播放进度
                if (initialTimeValue > 0 && audio.currentTime !== initialTimeValue) {{
                    audio.currentTime = initialTimeValue;
                }}
                
                pauseOtherPlayers(audio);
                
                // 5. 增加错误监听 (一次性)
                audio.addEventListener('error', () => {{
                    icon.className = 'fas fa-exclamation-triangle'; 
                    updatePlayingUI();
                    alert(`播放错误: 无法加载音源。请检查服务器文件或网络连接。`);
                }}, {{ once: true }});
                
                audio.play().catch(err => {{
                    console.warn('播放尝试失败:', err);
                    // 如果播放失败，恢复播放图标
                    icon.className = 'fas fa-play'; 
                    updatePlayingUI();
                }});
            }};

            // 播放/暂停按钮
            button.addEventListener('click', (e) => {{
                e.stopPropagation();
                if (audio.paused) {{
                    loadAndPlay();
                }} else {{
                    audio.pause();
                }}
            }});
            // =========================================================

            
            // 进度条更新
            audio.addEventListener('timeupdate', () => {{
                if (duration) {{
                    const percent = (audio.currentTime / duration) * 100;
                    progressBar.style.width = `${{percent}}%`;
                    currentTimeEl.textContent = formatTime(audio.currentTime);
                    
                    if (!audio.paused && audio.currentTime % 10 < 0.5) {{
                        saveEpisodeProgress(audioUrl, audio.currentTime, duration);
                    }}
                }}
            }});

            // 进度条拖动
            progressContainer.addEventListener('click', (e) => {{
                if (!audio.src) {{
                    loadAndPlay();
                    // 首次加载后用户需要再次点击以拖动
                    return; 
                }}
                if (duration) {{
                    const rect = progressContainer.getBoundingClientRect();
                    const percent = (e.clientX - rect.left) / rect.width;
                    audio.currentTime = percent * duration;
                }}
            }});

            audio.addEventListener('play', () => {{
                pauseOtherPlayers(audio);
                updatePlayingUI();
            }});

            audio.addEventListener('pause', () => {{
                updatePlayingUI();
                saveEpisodeProgress(audioUrl, audio.currentTime, duration);
            }});

            audio.addEventListener('ended', () => {{
                updatePlayingUI();
                // 播放结束后清除进度
                saveEpisodeProgress(audioUrl, duration, duration); 
            }});


            EPISODE_LIST.appendChild(listItem);
        }});
    }}

    window.addEventListener('beforeunload', () => {{
        allAudioPlayers.forEach(audio => {{
            // 只有当音频源已加载，且不是暂停状态时才保存
            if (audio.src && !audio.paused) {{
                const url = audio.dataset.audioUrl;
                const duration = parseFloat(audio.dataset.duration);
                saveEpisodeProgress(url, audio.currentTime, duration);
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

        logging.info(f"\n✅ **怀旧复古版 HTML (分季播放器 V8 - 性能优化)** 已成功生成: {html_output_path}")
        logging.info(f"请上传至服务器,访问 URL: {rss_url.replace('podcast.xml', 'index.html')}")
    except Exception as e:
        logging.error(f"❌ 生成 HTML 文件时出错: {e}")