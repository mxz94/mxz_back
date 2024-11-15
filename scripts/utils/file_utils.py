import json
import os

import requests


# 读取文件夹下所有文件
class FileUtils:
    @staticmethod
    def chek_file(file_path, content=None):
        path, file_name = os.path.split(file_path)
        if not os.path.exists(path):
            # 如果文件不存在，使用open()函数以写入模式创建文件
            os.makedirs(path)
        if not os.path.exists(file_path):
            # 如果文件不存在，使用open()函数以写入模式创建文件
            with open(file_path, 'w') as file:
                if content is None:
                    pass
                file.write(content)
    @staticmethod
    def read_all_file(path):
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    @staticmethod
    def write_json(file_path:str, data) -> str:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data))

    @staticmethod
    def rename_prefix(file, prefix):
        new_filename = file.replace(prefix,"")
        os.rename(file, new_filename)

    @staticmethod
    def compress_files_and_folders(zip_filename, files, folders):
        """
        压缩指定的文件和文件夹到ZIP文件中。

        :param zip_filename: str, ZIP文件的输出路径及名称。
        :param files: list, 单个文件的路径列表。
        :param folders: list, 要压缩的文件夹路径列表。
        """
        from zipfile import ZipFile
        with ZipFile(zip_filename, 'w') as zipf:
            # 添加文件
            for file in files:
                if os.path.isfile(file):
                    zipf.write(file, os.path.basename(file))

            # 压缩文件夹及其内容
            for root, dirs, filenames in os.walk(folders):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    zipf.write(file_path, file_path)
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


def notice_ding(title, content):
    json_data = {"title":title,"content":content,}
    response = requests.post('https://xizhi.qqoq.net/XZb02fde849963687f64a219eafba83a6b.send', json=json_data)
    print(response.json())


if __name__ == '__main__':
    FileUtils.compress_files_and_folders("./demo.zip", [], r"D:\mxz\mxz_back")