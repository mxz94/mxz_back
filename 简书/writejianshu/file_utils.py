import base64
import datetime
import hashlib
import hmac
import os
import re
import urllib

import requests

folder_path = "../note_o/2023"
IMG_DIR = "../img"
class FileUtil:
    @staticmethod
    def get_last_file():
        files = os.listdir(folder_path)

        # 排序文件列表，按修改时间降序排列
        files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)

        # 获取最新的文件（第一个文件）
        if files:
            latest_file = files[0]
            latest_file_path = os.path.join(folder_path, latest_file)
            new_file_path = latest_file_path
            date = str(datetime.date.today())
            if not latest_file.startswith('20'):
                new_file_path = os.path.join(folder_path, date +"({})".format(latest_file.split(".")[0]) + ".md")
                os.rename(latest_file_path, new_file_path)
            return new_file_path
        else:
            print("文件夹为空")

    @staticmethod
    def read_file(file_path:str):
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
        return file_contents

    @staticmethod
    def write_file(file_path:str, content: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def run_cmd( cmd_str='', echo_print=1):
        """
        执行cmd命令，不显示执行过程中弹出的黑框
        备注：subprocess.run()函数会将本来打印到cmd上的内容打印到python执行界面上，所以避免了出现cmd弹出框的问题
        :param cmd_str: 执行的cmd命令
        :return:
        """
        from subprocess import run
        if echo_print == 1:
            print('\n执行cmd指令="{}"'.format(cmd_str))
        run(cmd_str, shell=True)

    @staticmethod
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
                    FileUtil.download_image_file(img_url)
                    content = content.replace(img_url, os.path.join("../"+IMG_DIR, os.path.basename(img_url)))
                except Exception as e:
                    print("[ 不合法的 image url]:" + img_url)

            else:
                print("[ 不合法的 image url]:" + img_url)
        return content

    @staticmethod
    def download_image_file(url):
        r = requests.get(url)
        file = os.path.join(IMG_DIR, os.path.basename(url))
        with open(file, 'wb') as f:
            f.write(r.content)
            print(" # 写入DONE")
        return

