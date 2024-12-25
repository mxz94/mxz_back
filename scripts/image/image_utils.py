from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener
import os

register_heif_opener()

def compress_image(image):
    import tinify
    tinify.key = "FrPpqqhhsrj2zWmbqyTH6z7xl7MMfC1K"

    source = tinify.from_file(image)
    copyrighted = source.preserve("copyright", "creation", "location")
    copyrighted.to_file(image)

def convert_heic_to_jpg_and_upload(input_file):
    """
    将单个 HEIC 文件转换为 JPG 格式，并上传到七牛云，输出文件与输入文件在同一目录。
    如果文件不是 HEIC 格式，则不进行处理。

    :param input_file: 输入文件路径
    """
    if not input_file.lower().endswith('.heic'):
        print(f"文件 {input_file} 不是 HEIC 格式，跳过处理。")
        return

    # 打开 HEIC 文件
    img = Image.open(input_file)

    # 获取 EXIF 和 ICC 配置信息
    exif = img.info.get('exif')
    icc_profile = img.info.get('icc_profile')

    # 构建输出文件路径
    output_file = os.path.splitext(input_file)[0] + '.jpg'

    # 保存为 JPG 格式
    img.save(output_file, exif=exif, icc_profile=icc_profile)
    print(f"转换完成: {output_file}")


    # 上传转换后的 JPG 文件
    upload_url = upload_image_R2(output_file)
    print(f"上传完成: {upload_url}")

def resize_and_adjust_quality2(input_file, scale=0.3, quality=50):
    # 检查文件是否为图像
    if os.path.isfile(input_file) and input_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        with Image.open(input_file) as img:
            # 获取原始尺寸
            original_width, original_height = img.size

            # 计算新的尺寸（等比例缩放）
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            # 缩放图像
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # 保存图像，设置质量
            resized_img.save(input_file, quality=quality)

def upload_image_R2(file:str, prefix= None):
    from botocore.config import Config
    import boto3
    # 访问密钥 ID
    access_key = 'ad692e01f74450943b4122a84164835e'
    # 机密访问密钥
    secret_key = "fcba81ff9094e0204be641cb4e80e78660f43278aecf65e4433aa9a7ac6becf8"
    # 存储桶的 URL
    url = 'https://52666f83ef7dec7e1f33bc0afc91c693.r2.cloudflarestorage.com'
    filename = Path(file).name

    # 创建一个 S3 客户端，这里指定了 R2 的端点
    config = Config(signature_version='s3v4')
    s3_client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=url,
        config=config
    )
    # 你要上传到存储桶的名字
    bucket_name = 'mxz'
    # 本地文件 文件名
    bucket_file_name = f'dd/{filename}'
    if prefix:
        bucket_file_name = f'dd/{prefix}/{filename}'
        # 使用 S3 客户端上传文件
        s3_client.upload_file(file, bucket_name, bucket_file_name)
    else:
        s3_client.upload_file(file, bucket_name, bucket_file_name)
        resize_and_adjust_quality2(file)
        upload_image_R2(file, "thumbnail")


    return "https://pub-4232cd0528364004a537285f400807bf.r2.dev/" + bucket_file_name

def resize_and_adjust_quality(input_folder, output_folder, scale=0.3, quality=50):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # 检查文件是否为图像
        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            with Image.open(input_path) as img:
                # 获取原始尺寸
                original_width, original_height = img.size

                # 计算新的尺寸（等比例缩放）
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)

                # 缩放图像
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                # 构建输出路径
                output_path = os.path.join(output_folder, filename)

                # 保存图像，设置质量
                resized_img.save(output_path, quality=quality)
                print(f"Processed {filename} and saved to {output_path}")

def get_image_info(input_file):
    """
    将单个 HEIC 文件转换为 JPG 格式，并上传到七牛云，输出文件与输入文件在同一目录。
    如果文件不是 HEIC 格式，则不进行处理。

    :param input_file: 输入文件路径
    """
    if not input_file.lower().endswith('.heic'):
        print(f"文件 {input_file} 不是 HEIC 格式，跳过处理。")
        return

    # 打开 HEIC 文件
    img = Image.open(input_file)

    # 获取exif信息
    exif = img._getexif()
    
    if exif:
        # 提取GPS信息
        gps_info = exif.get(34853)
        if gps_info:
            # 提取经度和纬度
            gps_latitude = gps_info[2]
            gps_longitude = gps_info[4]

            # 将经纬度转换为十进制格式
            def convert_to_degrees(value):
                d = float(value[0])
                m = float(value[1])
                s = float(value[2])
                return d + (m / 60.0) + (s / 3600.0)

            lat = convert_to_degrees(gps_latitude)
            lon = convert_to_degrees(gps_longitude)

            # 如果是南纬或西经，需要取反
            if gps_info[1] == 'S':
                lat = -lat
            if gps_info[3] == 'W':
                lon = -lon

            return (lon, lat)
        else:
            return ("没有GPS信息",)
    else:
        return ("没有exif信息",)

# # 使用示例
# input_folder = r'D:\mxz\mxz_back\scripts\image\plog'
# output_folder = r'D:\mxz\mxz_back\scripts\image\thumbnail'
# resize_and_adjust_quality(input_folder, output_folder)

if __name__ == '__main__':
    print(get_image_info(r'C:\Users\Administrator\Downloads\IMG_1208.HEIC'))