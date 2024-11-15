import os

import requests


def download_image_file(url, file_name):
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)
        print(" # 写入DONE")

def comp_url_down(url, path):
    import requests
    json_data = {
        'source': {
            'url': url,
        },
    }
    response = requests.post('https://api.tinify.com/shrink', headers={'Content-Type': 'application/json'}, json=json_data, auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    response = requests.get(response.json()["output"]["url"], auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    with open(path, 'wb') as f:
        f.write(response.content)
def comp_path(path):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    with open(path, 'rb') as f:
        data = f.read()

    response = requests.post('https://api.tinify.com/shrink', headers=headers, data=data, auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    return response.json()["output"]["url"]

def comp_url_down_new(url, path):
    import tinify
    tinify.key = "CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl"
    new_width, new_height = calculate_new_size_from_url(url, target_width=1280)
    source = tinify.from_file(url)
    resized = source.resize(
        method="fit",
        width=new_width,
        height=new_height
    )
    converted = resized.convert(type=["image/png"])
    extension = converted.result().extension
    converted.to_file(path + "." + extension)
    # resized.to_file(path)
    return extension

def calculate_new_size_from_url(file, target_width=None, target_height=None):
    from io import BytesIO
    from PIL import Image

    # 将内容转换为图片对象
    img = Image.open(file)

    # 获取原始分辨率
    original_width, original_height = img.size

    # 根据目标宽度或高度计算新尺寸
    if target_width is not None:
        ratio = target_width / original_width
        new_height = int(original_height * ratio)
        return target_width, new_height

    elif target_height is not None:
        ratio = target_height / original_height
        new_width = int(original_width * ratio)
        return new_width, target_height

    else:
        return original_width, original_height

def down_com_img(url, path):
    print(url)
    response = requests.get(url, auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    with open(path, 'wb') as f:
        f.write(response.content)
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
from PIL import Image

def compress_image(input_image_path, output_image_path, quality=85):
    """
    压缩图片并保存到指定路径。

    :param input_image_path: 输入图片的路径
    :param output_image_path: 输出压缩图片的路径
    :param quality: 压缩质量（1到100，值越大质量越高，文件越大）
    """
    # 打开图片
    with Image.open(input_image_path) as img:
        # 压缩图片
        img.save(output_image_path, "JPEG", optimize=True, quality=quality)

import os
import zipfile

import os
import zipfile

import os

import os
import subprocess

def extract_7z_with_bandizip(source_dir, target_dir):
    """
    使用 Bandizip 解压 source_dir 中的所有 .7z 压缩文件到 target_dir，不保留目录结构。
    在解压前检查是否有 .7z 文件，并输出相关的调试信息。

    :param source_dir: 压缩文件所在的目录
    :param target_dir: 解压后的目标目录
    """
    # Bandizip 可执行文件的路径，确认 Bandizip 安装路径正确
    bandizip_executable = "bz"  # 或者 "C:\\Program Files\\Bandizip\\bz.exe"

    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历 source_dir 中的所有文件，检查是否有 .7z 文件
    found_7z_files = False
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".7z"):  # 只处理 .7z 文件
                found_7z_files = True
                archive_path = os.path.join(root, file)

                # 调试信息：输出正在处理的文件路径
                print(f"正在解压文件: {archive_path}")

                # 使用 subprocess 调用 Bandizip 命令行工具解压
                try:
                    command = [bandizip_executable, 'x', archive_path, '-o:' + target_dir, '-y']
                    subprocess.run(command, check=True)
                    print(f"解压成功: {archive_path}")
                except subprocess.CalledProcessError as e:
                    print(f"解压失败: {archive_path}. 错误: {e}")
                except Exception as e:
                    print(f"遇到其他错误: {e}")

    if not found_7z_files:
        print("没有找到任何 .7z 文件进行解压。")







if __name__ == '__main__':
    source_directory = r"E:\易默麒\n"  # 包含压缩文件的目录
    target_directory = r"E:\nn"   # 解压后的文件存放目录
    extract_7z_with_bandizip(source_directory, target_directory)
    # for f in os.listdir(r"E:\易默麒\11"):
    #     p = os.path.join(r"E:\易默麒\11", f)
    #     print(p)
    #     compress_image(p, os.path.join(r"E:\易默麒\22", f), 20 )
