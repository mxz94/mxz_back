import os
import shutil
from datetime import datetime

import piexif
from PIL import Image

def create_exif_data(date):
    exif_data = {
        'Exif': {
            piexif.ExifIFD.DateTimeOriginal: date,  # Set the creation date and time
        },

        # 'GPS': {
        #     piexif.GPSIFD.GPSLatitudeRef: 'N',  # Latitude reference ('N' for North)
        #     piexif.GPSIFD.GPSLatitude: ((22, 1), (34, 1), (15, 1)),  # Latitude coordinates (degrees, minutes, seconds)
        #     piexif.GPSIFD.GPSLongitudeRef: 'E',  # Longitude reference ('E' for East)
        #     piexif.GPSIFD.GPSLongitude: ((113, 1), (52, 1), (47, 1)),  # Longitude coordinates (degrees, minutes, seconds)
        # },
        # Add other Exif tags and values as needed
    }
    return exif_data

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

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f
def read_exif(image_path):
    try:
        # 打开图片
        image = Image.open(image_path)
        # 获取 Exif 信息
        exif_info = image._getexif()
        if exif_info:
            print(exif_info)
        else:
            print("No Exif information found in the image.")
    except Exception as e:
        print(f"Error: {e}")
path = r"D:\tmp\p\2020\Camera"
files = findAllFile(path)

for file in files:
    read_exif(os.path.join(path, file))
    date_obj = datetime.datetime.strptime(file.split(".")[0], '%Y%m%d').date()
    formatted_date_str = date_obj.strftime('%Y-%m-%d')
    write_exif(os.path.join(path, file), create_exif_data(formatted_date_str))