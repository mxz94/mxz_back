import os

from scripts.utils.file_utils import FileUtils

os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'

def calculate_new_size_from_url(image_url, target_width=None, target_height=None):
    from io import BytesIO
    from PIL import Image
    import requests
    # 通过网络请求获取图片
    response = requests.get(image_url)
    response.raise_for_status()  # 检查是否成功获取图片

    # 将内容转换为图片对象
    img = Image.open(BytesIO(response.content))

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


def calculate_new_size(image_path, target_width=None, target_height=None):
    from io import BytesIO
    from PIL import Image
    # 打开图片
    with Image.open(image_path) as img:
        original_width, original_height = img.size

    # 如果给定目标宽度，计算等比例的高度
    if target_width is not None:
        ratio = target_width / original_width
        new_height = int(original_height * ratio)
        return target_width, new_height

    # 如果给定目标高度，计算等比例的宽度
    elif target_height is not None:
        ratio = target_height / original_height
        new_width = int(original_width * ratio)
        return new_width, target_height

    # 如果都没有提供，返回原始尺寸
    else:
        return original_width, original_height

def comp_url_down(url, path):
    import tinify
    # tinify.key = "CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl"
    tinify.key = "4TvVJZQd399HDvCRmyfJmQCmNbSBqCGh"
    tinify.key = "FrPpqqhhsrj2zWmbqyTH6z7xl7MMfC1K"
    new_width, new_height = calculate_new_size(url, target_width=1200)
    source = tinify.from_file(url)
    resized = source.resize(
        method="cover",
        width=136,
        height=136
    )
    converted = resized.convert(type=["image/webp","image/png"])
    extension = converted.result().extension
    converted.to_file(path + "." + extension)
    # resized.to_file(path)
    # return path + "." + extension

# comp_url_down(r"https://github.com/user-attachments/assets/76793e36-20de-4e51-a1f6-dc8e6a3e2074", r"E:\mxz\dd2.jpg")

l = FileUtils.read_all_file(r"E:\ddd")
for i in l:
    comp_url_down(i, i.replace("ddd", "dd3"))