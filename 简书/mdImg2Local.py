import os
import re
import glob

import requests
import sys
DIR = "./files"
DIR_NEW = "./files"
IMG_DIR = "../img"
args = sys.argv
if len(args) == 2:
    DIR_NEW = DIR = args[1]
if len (args) == 3:
    DIR = args[1]
    DIR_NEW = args[2]

def process_content_new(content):
    if content == '':
        return
    img_list = re.findall(r"\!\[[^\]]*\]\((.+?)\)", content, re.S)
    flag = 0
    for iu in img_list:
        img_url = iu.split('?')[0]
        print('[Process:]' + img_url)
        if img_url.startswith(('http://', 'https://')):
            flag = 1
            try:
                download_image_file(img_url)
                content = content.replace(img_url, os.path.join("../"+IMG_DIR, os.path.basename(img_url)))
            except Exception as e:
                print("[ 不合法的 image url]:" + img_url)

        else:
            print("[ 不合法的 image url]:" + img_url)
    return content

def process_content(content, path):
    if content == '':
        return
    img_list = re.findall(r"\!\[[^\]]*\]\((.+?)\)", content, re.S)
    flag = 0
    for iu in img_list:
        img_url = iu.split('?')[0]
        print('[Process:]' + img_url)
        if img_url.startswith(('http://', 'https://')):
            flag = 1
            try:
                download_image_file(img_url)
                content = content.replace(img_url, "." + os.path.join(IMG_DIR, os.path.basename(img_url)))
            except Exception as e:
                print("[ 不合法的 image url]:" + img_url)

        else:
            print("[ 不合法的 image url]:" + img_url)
    # 文件夹相同且没有更新则不操作文件
    if DIR == DIR_NEW and flag == 0:
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def download_image_file(url):
    r = requests.get(url)
    file = os.path.join(IMG_DIR, os.path.basename(url))
    with open(file, 'wb') as f:
        f.write(r.content)
        print(" # 写入DONE")
    return


def read_file():
    # 读取文件夹下所有文件
    file_pattern = os.path.join(DIR, "*.md")
    files = glob.glob(file_pattern)
    for file in files:
        with open(file, "r", encoding='utf-8') as f:
            content = f.read()
        process_content(content, file.replace(DIR, DIR_NEW), IMG_DIR)


if __name__ == '__main__':
    read_file()