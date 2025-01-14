import os

from baiduImgSpider import baiduImgDownloader, im
from scripts.image.image_utils import get_image_info, convert_heic_to_jpg_and_upload, copy_exif

YourAK = "M7olmu7pXDVznsM1CdEXTG66B4hl4jWq"
ak = "mYL7zDrHfcb0ziXBqhBOcqFefrbRUnuq"

# baiduImgDownloader("resources/example_pandas.csv", # CRS: WGS84
#                     "resources/downloadPic", # folder
#                     ak=YourAK, zoom=4)
# convert_heic_to_jpg_and_upload(r'E:\CloudMusic\222\IMG_5678.HEIC')
# data = get_image_info(r'E:\CloudMusic\222\IMG_5678.jpg')
# im(f"{data[0]},{data[1]}", "resources/downloadPic", ak, zoom=4)

copy_exif(r'E:\CloudMusic\222\IMG_5678.HEIC', "resources/downloadPic/00000.jpg")