import os

import requests


# 读取文件夹下所有文件
class FileUtils:
    @staticmethod
    def read_all_file(path):
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

class Options:
    def __init__(self, options_dict):
        for key, value in options_dict.items():
            if isinstance(value, list):
                l = []
                for item in value:
                    l.append(Options(item))
                value = l
            setattr(self, key, value)

def download_image_file(url, file):
    r = requests.get(url)
    with open(file, 'wb') as f:
        f.write(r.content)
        print(" # 写入DONE")
    return

if __name__ == '__main__':
    print(FileUtils.read_all_file(r"D:\mxz\docker"))