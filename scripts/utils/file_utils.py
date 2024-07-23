import json
import os

import requests
from qiniu import Auth, put_file


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

def upload_image_file(file):
    try:
        access_key = "Y07Awc_13lhWdx-VS3Z78uCYxvgHDf19FJ4ousBc"
        secret_key = "3mD6dDLqur1M9yKoZG53qov-JS-7WVkOBD0SoeGj"
        url = "http://s9yka7j04.sabkt.gdipper.com/"
        q = Auth(access_key, secret_key)
        bucket_name = 'mxz9'
        #上传后保存的文件名
        path, name = os.path.split(file)
        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, name, 3600)
        #要上传文件的本地路径
        ret, info = put_file(token, name, file, version='v2')
        return url + name
    except Exception as e:
        print(" # 上传失败")
        return None

def notice_ding(title, content):
    json_data = {"title":title,"content":content,}
    response = requests.post('https://xizhi.qqoq.net/XZb02fde849963687f64a219eafba83a6b.send', json=json_data)
    print(response.json())


if __name__ == '__main__':
    file = r"D:\我的文档\Pictures\关羽长城骑摩托.jpg"
    url = upload_image_file(file)
    notice_ding("已成功拍照并保存到目录2", "![]({})".format(url))