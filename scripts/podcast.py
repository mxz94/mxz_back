import os
import datetime
import subprocess
import logging
import re
# 使用原生 XML 库代替 feedgen，提高稳定性
import xml.etree.ElementTree as ET
from xml.dom import minidom
# Mutagen 用于读取音频元数据
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
# from mutagen.ogg import OggFileType # OGG 文件支持可以按需添加
# tqdm 用于显示进度条
from tqdm import tqdm

from scripts.podcast_index import generate_player_html_new

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义 iTunes 命名空间常量
ITUNES_NS = 'http://www.itunes.com/dtds/podcast-1.0.dtd'

# ============== 配置信息 (请修改以下内容) ==============
# 播客名称 (用于文件夹和 URL)
PODCAST_TITLE = ""
# 存放播客音频文件的本地根目录
AUDIO_ROOT_DIR = r"E:\2"
# 您的服务器域名，所有播客链接的前缀 (使用 HTTPS 是最佳实践)
BASE_URL = f"https://malanxi.top/podcast_files/{PODCAST_TITLE}/"

# 输出的 RSS 文件名 (将放置在 AUDIO_ROOT_DIR 目录下)
OUTPUT_FILE = "podcast.xml"

# 播客整体信息
PODCAST_AUTHOR = "袁腾飞"
PODCAST_DESCRIPTION = PODCAST_TITLE
PODCAST_EMAIL = "your-email@example.com"
# 播客封面图片 URL (必须是 JPEG 或 PNG 格式，建议尺寸 1400x1400 到 3000x3000)
PODCAST_IMAGE_URL = BASE_URL + "cover.jpg"
PODCAST_CATEGORY = "Literature"
PODCAST_SUB_CATEGORY = "Books"

# 允许的音频文件扩展名
ALLOWED_EXTENSIONS = ('.mp3', '.m4a', '.mp4')
# 需要转码的格式
CONVERT_EXTENSIONS = ('.wma', '.flac', '.ogg', '.wav')

# =======================================================

def get_audio_duration(file_path):
    """使用mutagen尝试获取音频时长和文件大小。"""
    try:
        # 简化类型判断，使用 lower() 避免大小写问题
        path_lower = file_path.lower()
        if path_lower.endswith('.mp3'):
            audio = MP3(file_path)
        elif path_lower.endswith(('.m4a', '.mp4')):
            audio = MP4(file_path)
        elif path_lower.endswith('.flac'):
            audio = FLAC(file_path)
        else:
            # 忽略其他不确定能否读取元数据的格式
            return None, None

        duration = int(audio.info.length)
        size = os.path.getsize(file_path)
        return duration, size

    except Exception:
        # 无法读取元数据时，静默返回 None
        return None, None

def convert_to_mp3(wma_path):
    """
    使用 FFmpeg 将其他格式转换为 MP3。
    采用 -q:a 6 (高质量，约 120kbps) 压缩。
    """
    mp3_path = os.path.splitext(wma_path)[0] + '.mp3'

    if os.path.exists(mp3_path):
        # logging.info(f"MP3 文件已存在，跳过转码: {mp3_path}")
        return mp3_path

    logging.info(f"正在转码: {wma_path} -> {mp3_path}")

    command = [
        'ffmpeg',
        '-i', wma_path,
        '-vn', # 禁用视频
        '-acodec', 'libmp3lame',
        '-q:a', '6', # 高质量压缩
        mp3_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(wma_path)
        logging.info(f"✅ 转码成功并删除原文件: {wma_path}")
        return mp3_path
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ FFmpeg 转码失败: {wma_path}. 错误: {e}")
        return None
    except FileNotFoundError:
        logging.error("❌ FFmpeg 未安装或不在系统 PATH 中。请先安装 FFmpeg。")
        return None


def extract_season_info(folder_name):
    """
    从文件夹名称中提取季度信息。
    返回: (season_number, season_display_name)
    
    示例:
    - "第1季" -> (1, "第1季")
    - "Season 2" -> (2, "Season 2")  
    - "S03 三国演义" -> (3, "S03 三国演义")
    - "水浒传" -> (None, "水浒传")
    """
    # 尝试匹配各种季度格式
    patterns = [
        r'第(\d+)季',           # 第1季, 第2季
        r'[Ss]eason\s*(\d+)',   # Season 1, season 2
        r'[Ss](\d+)',           # S1, S01, s1
        r'^(\d+)',              # 纯数字开头
    ]

    for pattern in patterns:
        match = re.search(pattern, folder_name)
        if match:
            season_num = int(match.group(1))
            return season_num, folder_name

    # 如果没有匹配到数字，返回 None 和文件夹名
    return None, folder_name


def natural_sort_key(file_path):
    """
    自然排序键函数，用于正确排序包含数字的文件名。
    
    示例:
    - "2.xxx.mp3" 会排在 "10.xxx.mp3" 前面
    - "易中天品三国01.mp3" 会排在 "易中天品三国10.mp3" 前面
    - "40.（四十）赵高之死.mp3" 按数字 40 排序
    """
    # 获取文件名（不含路径）
    basename = os.path.basename(file_path)
    
    # 将文件名分割为文本和数字部分
    # 例如: "40.（四十）赵高之死.mp3" -> ['', '40', '.（四十）赵高之死.mp3']
    parts = re.split(r'(\d+)', basename)
    
    # 将数字部分转换为整数，便于正确排序
    result = []
    for part in parts:
        if part.isdigit():
            result.append(int(part))  # 数字部分转为整数
        else:
            result.append(part.lower())  # 文本部分转为小写（不区分大小写）
    
    return result


def generate_podcast_feed():
    """递归扫描目录、转码并生成播客 RSS 订阅源文件（使用原生 XML 模式）。"""

    logging.info("--- 播客 RSS 自动生成脚本开始（原生XML模式 + 智能Season识别 + 自然排序）---")

    # 1. 扫描文件并进行转码
    all_files_to_process = []
    for root, _, files in os.walk(AUDIO_ROOT_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            if ext in CONVERT_EXTENSIONS:
                mp3_path = convert_to_mp3(file_path)
                if mp3_path:
                    all_files_to_process.append(mp3_path)
            elif ext in ALLOWED_EXTENSIONS:
                all_files_to_process.append(file_path)

    # 【改进：使用自然排序，确保"2."排在"10."前面】
    all_files_to_process = sorted(all_files_to_process, key=natural_sort_key)
    
    if not all_files_to_process:
        logging.warning("未找到任何音频文件。")
        return

    logging.info(f"找到 {len(all_files_to_process)} 个文件准备生成 RSS。")

    # 【新增：检测是否有多个文件夹，决定是否使用季度功能】
    unique_folders = set()
    for file_path in all_files_to_process:
        relative_dir = os.path.relpath(os.path.dirname(file_path), AUDIO_ROOT_DIR)
        if relative_dir == '.':
            unique_folders.add('_root_')  # 根目录标记
        else:
            folder_name = relative_dir.replace('\\', '/').split('/')[0]
            unique_folders.add(folder_name)

    use_seasons = len(unique_folders) > 1  # 只有多个文件夹时才使用季度

    if use_seasons:
        logging.info(f"📁 检测到 {len(unique_folders)} 个文件夹，将使用季度功能分组")
    else:
        logging.info("📁 单文件夹播客，不使用季度功能")

    # 2. 构造 XML 结构 (命名空间修复点)

    # 【修复：使用 register_namespace 避免命名空间冲突】
    # 预先注册命名空间，让 ElementTree 自动在根元素上添加 xmlns:itunes
    ET.register_namespace('itunes', ITUNES_NS)

    # 创建根元素，不再手动添加 xmlns:itunes 属性，只添加 version="2.0"
    rss = ET.Element('rss', version='2.0')

    channel = ET.SubElement(rss, 'channel')

    # 播客频道信息
    ET.SubElement(channel, 'title').text = PODCAST_TITLE
    ET.SubElement(channel, 'link').text = BASE_URL
    ET.SubElement(channel, 'description').text = PODCAST_DESCRIPTION
    ET.SubElement(channel, 'language').text = 'zh-cn'

    # ITunes 频道标签 (使用命名空间URI方式添加标签)
    ET.SubElement(channel, f'{{{ITUNES_NS}}}author').text = PODCAST_AUTHOR
    ET.SubElement(channel, f'{{{ITUNES_NS}}}type').text = 'serial'
    ET.SubElement(channel, f'{{{ITUNES_NS}}}image', attrib={'href': PODCAST_IMAGE_URL})
    ET.SubElement(channel, f'{{{ITUNES_NS}}}explicit').text = 'no'
    ET.SubElement(channel, f'{{{ITUNES_NS}}}owner').text = PODCAST_EMAIL

    # Category 标签
    category = ET.SubElement(channel, f'{{{ITUNES_NS}}}category', attrib={'text': PODCAST_CATEGORY})
    if PODCAST_SUB_CATEGORY:
        ET.SubElement(category, f'{{{ITUNES_NS}}}category', attrib={'text': PODCAST_SUB_CATEGORY})

    # 3. 遍历文件并添加单集
    for local_path in tqdm(all_files_to_process, desc="生成 RSS 条目"):

        relative_path = os.path.relpath(local_path, AUDIO_ROOT_DIR).replace('\\', '/')
        file_url = BASE_URL + relative_path
        duration_seconds, file_size_bytes = get_audio_duration(local_path)

        if duration_seconds is None or file_size_bytes is None:
            continue

        episode_title = os.path.splitext(os.path.basename(local_path))[0]
        # 确保时区信息正确，符合 RSS 规范
        pub_date_str = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%a, %d %b %Y %H:%M:%S %z")

        # 创建 item 元素
        item = ET.SubElement(channel, 'item')

        # 【根据是否使用季度功能决定标题格式】
        if use_seasons:
            # 【智能文件夹分季逻辑】
            relative_dir = os.path.relpath(os.path.dirname(local_path), AUDIO_ROOT_DIR)

            if relative_dir == '.':
                # 根目录下的文件视为第 1 季
                season_number = 1
                season_name = None
            else:
                # 使用一级子文件夹名提取季度信息
                folder_name = relative_dir.replace('\\', '/').split('/')[0]
                season_number, season_name = extract_season_info(folder_name)

                # 如果无法提取数字，默认使用 1
                if season_number is None:
                    season_number = 1

            # 【在标题中包含季度名称】
            if season_name:
                full_title = f"[{season_name}] {episode_title}"
            else:
                full_title = episode_title
        else:
            # 单文件夹，不添加季度信息
            full_title = episode_title
            season_number = None
            season_name = None

        ET.SubElement(item, 'title').text = full_title
        ET.SubElement(item, 'description').text = f"集数: {episode_title}"
        ET.SubElement(item, 'pubDate').text = pub_date_str

        # 核心：设置音频附件
        ET.SubElement(item, 'enclosure', attrib={
            'url': file_url,
            'length': str(file_size_bytes),
            'type': 'audio/mpeg'
        })

        # GUID
        ET.SubElement(item, 'guid').text = relative_path

        # ITunes 剧集标签
        ET.SubElement(item, f'{{{ITUNES_NS}}}duration').text = str(duration_seconds)
        ET.SubElement(item, f'{{{ITUNES_NS}}}author').text = PODCAST_AUTHOR

        # 【只有使用季度功能时才添加 season 相关标签】
        if use_seasons and season_number is not None:
            ET.SubElement(item, f'{{{ITUNES_NS}}}season').text = str(season_number)

            # 【可选：添加 subtitle 显示季度完整名称】
            if season_name:
                ET.SubElement(item, f'{{{ITUNES_NS}}}subtitle').text = season_name


    # 4. 格式化和保存 RSS 文件
    output_path = os.path.join(AUDIO_ROOT_DIR, OUTPUT_FILE)

    # 格式化
    xml_str = ET.tostring(rss, encoding='utf-8')
    reparsed = minidom.parseString(xml_str)

    # 修复 minidom 导致的前缀问题 (ET.register_namespace 已经处理了大部分，这里作为二次保险)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    pretty_xml = pretty_xml.replace('ns0:', 'itunes:')
    pretty_xml = pretty_xml.replace(f'xmlns:ns0="{ITUNES_NS}"', f'xmlns:itunes="{ITUNES_NS}"')

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # 确保 XML 声明的编码与文件编码一致
            if pretty_xml.startswith('<?xml'):
                f.write(pretty_xml)
            else:
                f.write('<?xml version="1.0" encoding="utf-8"?>\n' + pretty_xml)

        logging.info(f"\n✅ RSS 订阅源已成功生成到文件: {output_path}")
        logging.info(f"✅ 您的播客 RSS URL 为: {BASE_URL}{OUTPUT_FILE}")
        logging.info(f"🔢 文件已使用自然排序（数字顺序）")
        if use_seasons:
            logging.info(f"📱 iPhone Podcast 将显示文件夹名称作为季度信息")
        else:
            logging.info(f"📱 单文件夹播客，无季度分组")
    except Exception as e:
        logging.error(f"\n❌ 生成文件时出错: {e}")


def generate_player_html():
    """生成播客 HTML 播放器页面。"""
    rss_url_public = BASE_URL + OUTPUT_FILE
    html_output_path = os.path.join(AUDIO_ROOT_DIR, 'index.html')

    logging.info("--- 静态播放器 HTML 生成脚本开始 ---")

    generate_player_html_new(rss_url_public, PODCAST_TITLE, PODCAST_AUTHOR, PODCAST_IMAGE_URL, html_output_path)



if __name__ == '__main__':
    # 1. 先生成包含 Season 标签的 RSS 文件
    generate_podcast_feed()

    # 2. 再生成包含 Season 切换逻辑的 HTML 文件
    generate_player_html()