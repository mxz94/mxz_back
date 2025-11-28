import os
import subprocess
import logging
from tqdm import tqdm

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ============== 配置信息 (请修改以下内容) ==============

# 存放待处理音频文件的根目录 (脚本将递归扫描此目录及其子文件夹)
AUDIO_ROOT_DIR = r"E:\2" # 请改为您的实际目录

# 目标音频文件扩展名。我们现在只关注 MP3。
ALLOWED_EXTENSIONS = ('.mp3',)

# FFmpeg MP3 质量等级 (-q:a)。范围 0-9。
# 数字越大 = 压缩率越高 = 文件越小 = 质量越低。
# 建议：
# - 2 (约 190 kbps) - 高质量，文件较大
# - 4 (约 160 kbps) - 平衡，推荐用于播客/有声书
# - 6 (约 120 kbps) - 明显压缩，文件较小
COMPRESSION_QUALITY = '6' # 示例：使用 6 显著压缩文件

# 是否覆盖已存在的 MP3 文件？
# 为了压缩，我们必须设置为 True，因为它需要重新编码。
OVERWRITE_EXISTING = True

# =======================================================

def compress_mp3(mp3_path, compression_quality, overwrite=True):
    """
    使用 FFmpeg 对已有的 MP3 文件进行重新编码和压缩。

    (已修正：强制指定输出格式为 MP3，解决 'Unable to find a suitable output format' 错误)
    """

    temp_mp3_path = mp3_path + ".temp"

    logging.info(f"正在压缩: {os.path.basename(mp3_path)} (目标质量 -q:a {compression_quality})")

    # FFmpeg 命令：【关键修正：添加 -f mp3 明确指定输出格式，并使用 -c:a 指定编码器】
    command = [
        'ffmpeg',
        '-i', mp3_path,
        '-vn',
        '-c:a', 'libmp3lame', # 使用 -c:a 更明确地指定编码器
        '-q:a', str(compression_quality),
        '-f', 'mp3',          # 【修正】强制输出格式为 mp3
        '-y',
        temp_mp3_path
    ]

    try:
        # 1. 执行命令，将结果写入临时文件
        result = subprocess.run(command, check=True, capture_output=True)

        # 2. 成功后，删除原文件
        os.remove(mp3_path)

        # 3. 将临时文件重命名为原文件名
        os.rename(temp_mp3_path, mp3_path)

        logging.info(f"✅ 压缩成功并覆盖原文件: {os.path.basename(mp3_path)}")
        return mp3_path

    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode('utf-8', errors='ignore')

        if os.path.exists(temp_mp3_path):
            os.remove(temp_mp3_path)

        logging.error(f"❌ FFmpeg 压缩失败: {os.path.basename(mp3_path)}. 详细错误信息:")
        logging.error("--- FFmpeg Output ---")
        logging.error(error_output)
        logging.error("---------------------")
        return None
    except FileNotFoundError:
        logging.error("❌ FFmpeg 未安装或不在系统 PATH 中。请先安装 FFmpeg。")
        return None

def process_audio_directory(root_dir, allowed_extensions, quality, overwrite):
    """递归遍历目录，查找并处理音频文件。"""

    files_to_process = []

    # 1. 递归收集需要处理的文件列表
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            # 只处理 MP3 文件
            if ext in allowed_extensions:
                files_to_process.append(file_path)

    if not files_to_process:
        logging.warning(f"在目录 {root_dir} 中未找到任何 MP3 文件。")
        return

    logging.info(f"找到 {len(files_to_process)} 个 MP3 文件准备进行压缩...")

    # 2. 遍历列表并进行压缩，显示进度条
    processed_count = 0
    with tqdm(total=len(files_to_process), desc="压缩 MP3 文件") as pbar:
        for file_path in files_to_process:
            result_path = compress_mp3(file_path, quality, overwrite)
            if result_path:
                processed_count += 1
            pbar.update(1)

    logging.info(f"--- 压缩完成！共处理 {processed_count} 个文件。---")


if __name__ == '__main__':
    # 调用主处理函数
    # 注意：为了压缩，OVERWRITE_EXISTING 必须为 True。
    if not OVERWRITE_EXISTING:
        logging.error("配置错误：压缩 MP3 必须设置 OVERWRITE_EXISTING = True 才能重新编码。请修改配置。")
    else:
        process_audio_directory(
            root_dir=AUDIO_ROOT_DIR,
            allowed_extensions=ALLOWED_EXTENSIONS,
            quality=COMPRESSION_QUALITY,
            overwrite=OVERWRITE_EXISTING
        )