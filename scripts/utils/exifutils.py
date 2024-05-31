import os
import shutil
from datetime import datetime
import piexif
from PIL import Image, ExifTags

from datetime import datetime

def format_datetime(input_str):
    # 解析输入字符串为日期时间对象
    time_format = "%Y-%m-%d-%H-%M-%S-%f"
    dt = datetime.strptime(input_str, time_format)
    # 将日期时间对象格式化为目标格式
    formatted_str = dt.strftime("%Y:%m:%d %H:%M:%S")
    return formatted_str

def move_file(source_file, destination_folder):
    try:
        # Move the file to the destination folder
        shutil.move(source_file, destination_folder)
        print("File moved successfully.")
    except Exception as e:
        print(f"Error: {e}")

def write_exif(image_path, exif_data):
    try:
        # Open the image
        image = Image.open(image_path)

        # Encode the Exif data dictionary to bytes
        exif_bytes = piexif.dump(exif_data)

        # Update the Exif data in the image
        image.save(image_path, exif=exif_bytes)
        print("Exif data written successfully.")
    except Exception as e:
        print(f"Error: {e}")

BAOTI = {
    piexif.GPSIFD.GPSLatitudeRef: 'N',  # Latitude reference ('N' for North)
    piexif.GPSIFD.GPSLatitude: ((22, 1), (34, 1), (15, 1)),  # Latitude coordinates (degrees, minutes, seconds)
    piexif.GPSIFD.GPSLongitudeRef: 'E',  # Longitude reference ('E' for East)
    piexif.GPSIFD.GPSLongitude: ((113, 1), (52, 1), (47, 1)),  # Longitude coordinates (degrees, minutes, seconds)
}

GSW = {
    piexif.GPSIFD.GPSLatitudeRef: 'N',  # Latitude reference ('N' for North)
    piexif.GPSIFD.GPSLatitude: ((22, 1), (34, 1), (59, 1)),  # Latitude coordinates (degrees, minutes, seconds)
    piexif.GPSIFD.GPSLongitudeRef: 'E',  # Longitude reference ('E' for East)
    piexif.GPSIFD.GPSLongitude: ((113, 1), (51, 1), (33, 1)),  # Longitude coordinates (degrees, minutes, seconds)
}
HSL = {
    piexif.GPSIFD.GPSLatitudeRef: 'N',  # Latitude reference ('N' for North)
    piexif.GPSIFD.GPSLatitude: ((22, 1), (31, 1), (25, 1)),  # Latitude coordinates (degrees, minutes, seconds)
    piexif.GPSIFD.GPSLongitudeRef: 'E',  # Longitude reference ('E' for East)
    piexif.GPSIFD.GPSLongitude: ((113, 1), (59, 1), (41, 1)),  # Longitude coordinates (degrees, minutes, seconds)
}

KX = {
    piexif.GPSIFD.GPSLatitudeRef: 'N',  # Latitude reference ('N' for North)
    piexif.GPSIFD.GPSLatitude: ((22, 1), (32, 1), (38, 1)),  # Latitude coordinates (degrees, minutes, seconds)
    piexif.GPSIFD.GPSLongitudeRef: 'E',  # Longitude reference ('E' for East)
    piexif.GPSIFD.GPSLongitude: ((113, 1), (56, 1), (38, 1)),  # Longitude coordinates (degrees, minutes, seconds)
}

MC = {
    piexif.GPSIFD.GPSLatitudeRef: 'N',  # Latitude reference ('N' for North)
    piexif.GPSIFD.GPSLatitude: ((34, 1), (35, 1), (43, 1)),  # Latitude coordinates (degrees, minutes, seconds)
    piexif.GPSIFD.GPSLongitudeRef: 'E',  # Longitude reference ('E' for East)
    piexif.GPSIFD.GPSLongitude: ((112, 1), (30, 1), (33, 1)),  # Longitude coordinates (degrees, minutes, seconds)
}
def create_exif_data(date):
    # Specify the Exif data as a dictionary
    exif_data = {
        'Exif': {
            piexif.ExifIFD.DateTimeOriginal: date,  # Set the creation date and time
        }
        # Add other Exif tags and values as needed
    }
    return exif_data


from PIL import Image, ExifTags
s = []
def read_exif(image_path):
    try:
        # 打开图片
        image = Image.open(image_path)
        # 获取 Exif 信息
        exif_info = image._getexif()
        if exif_info:
            hasGPS = False
            for tag, value in exif_info.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    hasGPS = True
                    break
            if not hasGPS:
                s.append(image_path)
                move_file(image_path, move_to_path)
        else:
            move_file(image_path, move_to_path)
            print("No Exif information found in the image.")
    except Exception as e:
        print(f"Error: {e}")

# 调用函数进行转换

def filter_files_with_prefix(directory):
    files_with_prefix = []
    for filename in os.listdir(directory):
        if filename.startswith("Screenshot_"):
            datetime_digitized = filename.replace("Screenshot_", "")[:len("2020-08-24-12-20-16-52")]
            print(format_datetime(datetime_digitized))
            data = create_exif_data(format_datetime(datetime_digitized))
            write_exif(directory + "\\"+filename, data)
        # if filename.endswith(".jpg"):
        #     read_exif(directory + "\\"+filename)
    return files_with_prefix

# 指定目录路径和文件名前缀
directory_path = r"G:\mxz\DCIM\screen\2014-2016"  # 替换为实际的目录路径
move_to_path = r"G:\mxz\DCIM\2021-2022\diushi\nogps"
filter_files_with_prefix(directory_path)
print(len(s))
