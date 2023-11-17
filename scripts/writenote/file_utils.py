import os

import requests

from scripts.writenote.jian_utils_services import upload_image, upload_image_2


def download_image_file(url, filePath):
    r = requests.get(url)
    with open(filePath, 'wb') as f:
        f.write(r.content)
        print(" # 写入DONE")
    return

s = r"D:\mxz\mxz_back\src\content\img\6904315-837bb254719beb50.jpg"
url = upload_image_2(s)
download_image_file(url, s)
# for file in os.listdir(s):
#     url = upload_image(s + "/" + file)
#     download_image_file(url, s + "/" + file)