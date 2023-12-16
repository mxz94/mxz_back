import configparser
import datetime
import os
import re
import shutil
import time
from threading import Thread

import html2text
import qiniu
import requests
from github import Github, Repository

os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'


src = r"D:\mxz\mxz_back"

file = src + r'\scripts\writenote\config.ini'

img_path = src + r'\src\content\img'
file_path = src + r'\src\content\blog'

file_path_online = src + r'\scripts\writenote\content\note/'

prefix = """---
pubDatetime: {}
title: {}
tags:
  - "{}"
---

{}
"""

# 创建配置文件对象
con = configparser.ConfigParser()

# 读取文件
con.read(file, encoding='utf-8')

class GithubUtils:

    @staticmethod
    def get_repo(token: str, repo: str):
        return Github(token).get_repo(repo)


    @staticmethod
    def create_issue(repo: Repository, file: str):
        (filePath,name) = os.path.split(file)
        title = name.split(".")[0]
        label = title[:4] if title.startswith("20") else "1994"

        with open(file, "r", encoding="utf8") as f:
                content = f.read() + "\n" +  "[{}](https://github.com/{}/blob/master/src/content/blog/{}/{})".format(title, repo.full_name, label, name)
                repo.create_issue(title, content,labels = [label, "展望"])

class ConfigUtils:
    @staticmethod
    def get_now_day():
        return str(datetime.date.today())

    @staticmethod
    def get_now_str():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get(key:str, section='default'):
        items = con.items(section) 	# 返回结果为元组
        items = dict(items)
        return items.get(key)
    @staticmethod
    def set(key:str, value:str, section='default'):
        con.set(section, key, value )
        with open(file, 'w', encoding="utf-8") as configfile:
            con.write(configfile)

    @staticmethod
    def get_local(key:str, section='default'):
        con2 = configparser.ConfigParser()
        con2.read(ConfigUtils.get("local_config"), encoding='utf-8')
        items = con2.items(section) 	# 返回结果为元组
        items = dict(items)
        return items.get(key)

IMG_DIR = "../img"
IMG_DIR_2 = r"/content/img"
directory_path = r"/content/note_o"
dd = '''
<details {}><summary>{}</summary>
<p>

{}

</p>
</details>
'''
class FileUtil:

    @staticmethod
    def move_first_to_last(my_list):
        if len(my_list) >= 2:
            first_element = my_list.pop(0)
            my_list.append(first_element)
    @staticmethod
    def check_dir(dir:str):
        if not os.path.exists(dir):
            os.makedirs(dir)
    @staticmethod
    def get_last_file():
        year = ConfigUtils.get_now_day()[:4]
        folder_path = file_path + "/" + year
        files = os.listdir(folder_path)

        # 排序文件列表，按修改时间降序排列
        # files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
        files.sort(reverse=True)
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
    def process_content_new(content, on_line = False):
        if content == '':
            return
        if content.find("<p>") != -1:
            content = html2text.html2text(content)
        img_list = re.findall(r"\!\[[^\]]*\]\((.+?)\)", content, re.S)
        flag = 0
        for iu in img_list:
            img_url = iu.split('?')[0].replace("\n", '')
            print('[Process:]' + img_url)
            if on_line:
                content = content.replace(iu, img_url)
            else:
                if img_url.startswith(('http://', 'https://')):
                    flag = 1
                    try:
                        FileUtil.download_image_file(img_url)
                        content = content.replace(iu, "../"+IMG_DIR+ "/" + os.path.basename(img_url))
                    except Exception as e:
                        print("[ 不合法的 image url]:" + img_url)

                else:
                    print("[ 不合法的 image url]:" + img_url)
        return content

    @staticmethod
    def download_image_file(url, day=None):
        r = requests.get(url)
        end = os.path.basename(url).split(".")[1]
        file = os.path.join(IMG_DIR_2, "{}/{}.{}".format(day[:4], day, end) )
        with open(file, 'wb') as f:
            f.write(r.content)
            print(" # 写入DONE")
        return

    @staticmethod
    def init_readme(fileName = "README.md" , pg = "note_o"):
        FileUtil.init_o_readme("README.md", r"/src/content/blog")
        FileUtil.init_o_readme("README_JIAN.md", r"/scripts/writenote/content/note")
        FileUtil.init_oline_readme()

    @staticmethod
    def init_readme(fileName = "README.md", pg=r"/src/content/blog"):
        # 使用os.listdir()获取目录下所有文件和文件夹的列表
        file_names = os.listdir(src + pg)
        s = {}
        # 遍历文件名列表并打印
        for file_name in file_names:
            if not os.path.isfile(os.path.join(directory_path, file_name)):
                s[file_name] = []
                file_names2 = os.listdir(os.path.join(directory_path, file_name))
                for file_name2 in file_names2:
                    s[file_name].append("[{}]({})".format(file_name2.split(".")[0],   "./"+pg+"/"+ file_name + "/" + file_name2))

        re_s = reversed(s.items())
        for key, value in re_s:
            value.reverse()

        re_s = reversed(s.items())
        with open("D:\mxz\mxz_back\简书/"+ fileName, 'w', encoding='utf-8') as file:
            open2 = "open"
            for key, value in re_s:
                content = ""
                for item in value:
                    content += item + "<br>\n"
                    # file.write(item + "<br>\n")
                file.write(dd.format(open2,key, content))
                open2 = ""
    @staticmethod
    def init_archives_readme():
        url = "https://mxz-back.pages.dev/posts/"
        # 指定目录路径
        directory_path = src + r"\src\content\blog"
        # 使用os.listdir()获取目录下所有文件和文件夹的列表
        file_names = os.listdir(directory_path)
        s = {}
        # 遍历文件名列表并打印
        for file_name in file_names:
            if not os.path.isfile(os.path.join(directory_path, file_name)):
                s[file_name] = []
                file_names2 = []
                for  root, dirs, files in os.walk(os.path.join(directory_path, file_name)):
                    file_names2 += files
                for file_name2 in file_names2:
                    title = file_name2.split(".")[0]
                    u = title.replace("(", "").replace(")", "").replace("，","").replace(",","").replace("（", "").replace("）", "")
                    s[file_name].append("[{}]({})".format(title, url + u))

        re_s = reversed(s.items())
        for key, value in re_s:
            value.reverse()
            if key.startswith("20") and value[0].endswith("展望)"):
                FileUtil.move_first_to_last(value)

        re_s = reversed(s.items())

        start = '''---
layout: ../layouts/ArchivesLayout.astro
title: ""
---
'''
        dd = '''
# {}
        
{}
        
        '''
        file_path = src + r"\src\pages\archives.md"  # 替换为你想要创建的文件路径
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(start)
            for key, value in re_s:
                content = ""
                for item in value:
                    content += item + "<br>\n"
                file.write(dd.format(key, content))

    @staticmethod
    def init_oline_readme(fileName = "README_ONLINE.md"):
        try:
            data = note_list()
            s = {}
            # 遍历文件名列表并打印

            for item in data:
                title = item["title"].split(".")[0] + ".md"
                slug = item["slug"]
                year = title[:4]
                if s.get(year) is None:
                    s[year] = []
                s[year].append("[{}]({})".format(title.split(".")[0],   "https://www.jianshu.com/p/" + slug))
            re_s = s.items()
            with open("D:\mxz\mxz_back\简书/"+ fileName, 'w', encoding='utf-8') as file:
                open2 = "open"
                for key, value in re_s:
                    content = ""
                    for item in value:
                        content += item + "<br>\n"
                        # file.write(item + "<br>\n")
                    file.write(dd.format(open2,key, content))
                    open2 = ""
        except Exception as e:
         print(e)

    @staticmethod
    def notice_ding(title, content, link, time):
        json_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "简书：" + title,
                "text": "# {} \n\n".format(title) + "{}\n > ###### {}发布 [查看]({}) \n".format(content, time, link)
            }
        }
        response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=7fff5466a5711119b2059f1c65df3ab80c8a65025342f651c60c81618d9f4362', json=json_data)
        print(response.json())
    @staticmethod
    def notice_ding_error(e: str):
        json_data = {
            "at": {
                "atMobiles":[
                    "180xxxxxx"
                ],
                "atUserIds":[
                    "user123"
                ],
                "isAtAll": True
            },
            "text": {
                "content":f"简书`{e}`"
            },
            "msgtype":"text"
        }

        response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=04ae95082327176ae45c70859b70b8f3043fa143c46d587236f6ddecce117a4f', json=json_data)
        print(response.json())

    @staticmethod
    def notice_wechat(title: str):
        response = requests.get('https://sctapi.ftqq.com/SCT142512TIZeFu7Dj22drBfQgwT0KPIdI.send?title={}'.format(title))

DIR= r'/content/note/'
DIR_O= r'/content/note_o/'

def getCookies():
    import http.cookies
    import json

    cookie_str = "_ga=GA1.2.316202546.1695480391; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1699181179; _ga_Y1EKTCT110=GS1.2.1699183942.3.0.1699183942.0.0.0; read_mode=day; default_font=font2; locale=zh-CN; remember_user_token=W1s2OTA0MzE1XSwiJDJhJDEwJDRjbkxQOE9iSHZGeDRyT3hzMnpSek8iLCIxNzAwOTE0NDY2LjA4MjgxMiJd--8603698ab407f9a75724e1c5d4dcbca2bfd320ce; web_login_version=MTcwMDkxNDQ2Ng%3D%3D--74a54859ae71b706a9cbb6557bf6e889a828ee96; _m7e_session_core=0381aac27a41a47d706ce49ebf956bec; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%7D"

    cookies = http.cookies.SimpleCookie()
    cookies.load(cookie_str)

    cookie_dict = {}
    for key, morsel in cookies.items():
        cookie_dict[key] = morsel.value

    # 转换为 JSON 对象
    return  json.dumps(cookie_dict, ensure_ascii=False)


cookies = {
    '_ga': 'GA1.2.316202546.1695480391',
    'Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068': '1699181179',
    '_ga_Y1EKTCT110': 'GS1.2.1699183942.3.0.1699183942.0.0.0',
    'read_mode': 'day',
    'default_font': 'font2',
    'locale': 'zh-CN',
    'remember_user_token': 'W1s2OTA0MzE1XSwiJDJhJDEwJDRjbkxQOE9iSHZGeDRyT3hzMnpSek8iLCIxNzAwOTE0NDY2LjA4MjgxMiJd--8603698ab407f9a75724e1c5d4dcbca2bfd320ce',
    'web_login_version': 'MTcwMDkxNDQ2Ng%3D%3D--74a54859ae71b706a9cbb6557bf6e889a828ee96',
    '_m7e_session_core': '0381aac27a41a47d706ce49ebf956bec',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%7D',
}

headers = {
    'authority': 'www.jianshu.com',
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'cookie': '_ga=GA1.2.316202546.1695480391; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1699181179; _ga_Y1EKTCT110=GS1.2.1699183942.3.0.1699183942.0.0.0; read_mode=day; default_font=font2; locale=zh-CN; remember_user_token=W1s2OTA0MzE1XSwiJDJhJDEwJDRjbkxQOE9iSHZGeDRyT3hzMnpSek8iLCIxNzAwOTE0NDY2LjA4MjgxMiJd--8603698ab407f9a75724e1c5d4dcbca2bfd320ce; web_login_version=MTcwMDkxNDQ2Ng%3D%3D--74a54859ae71b706a9cbb6557bf6e889a828ee96; _m7e_session_core=0381aac27a41a47d706ce49ebf956bec; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%7D',
    'if-none-match': 'W/"4a70973d5c4e6e77e1b7944653a4b13d"',
    'referer': 'https://www.jianshu.com/writer',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def upload_image(file:str):
    (filepath, filename) = os.path.split(file)
    print(filename)
    params = {
        'filename': filename,
    }
    response = requests.get('https://www.jianshu.com/upload_images/token.json', params=params, cookies=cookies, headers=headers)
    data = response.json()
    ret, info = qiniu.put_file(data["token"], data["key"], img_path + "/{}/{}".format(filename[:4], filename))

    return ret['url']


def replace_img_url(content):
    pattern = r'\((.*?)\)'
    matchs = re.findall(pattern, content)
    for img_path in matchs:
        if file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png"):
            imgurl = upload_image(img_path)
            print(imgurl)
            FileUtil.download_image_file(imgurl, ConfigUtils.get_now_day())
            content= content.replace('({})'.format(img_path), '({})'.format(imgurl))
    return content

def create_article(title:str):
    json_data = {
        'notebook_id': '14385934',
        'title': title,
        'at_bottom': False,
    }
    response = requests.post('https://www.jianshu.com/author/notes', cookies=cookies, headers=headers, json=json_data)
    print("create_article" +  response.text)
    return response.json()

def publize(id):
    response = requests.post('https://www.jianshu.com/author/notes/{}/publicize'.format(id), cookies=cookies, headers=headers, json={})
    print("publize" +  response.text)
def write_content(content:str, id:str):
    json_data = {
        'id': id,
        'autosave_control': 1,
        'content': content,
    }
    response = requests.put('https://www.jianshu.com/author/notes/'+id, cookies=cookies, headers=headers, json=json_data)
    print("write_content" +  response.text)
    publize(id)

def get_content(id:str):
    response = requests.get('https://www.jianshu.com/author/notes/{}/content'.format(id), cookies=cookies, headers=headers)
    return response.json()["content"]



def note_list():
    response = requests.get('https://www.jianshu.com/author/notebooks/14385934/notes', cookies=cookies, headers=headers)
    return response.json()
def jianshu_to_local():
    (filepath, filename) = os.path.split(FileUtil.get_last_file())
    list = note_list()
    name = "title:"
    for new_article in list:
        title = new_article["title"].split(".")[0] + ".md"
        if title == filename:
            break;
        name = name +","+ title
        content = get_content(new_article["id"])
        on_content = FileUtil.process_content_new(content, True)
        FileUtil.write_file(DIR+title[:4]+"/"+ title, on_content)
        FileUtil.notice_ding(title, on_content, "https://www.jianshu.com/p/" + new_article["slug"], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_article["content_updated_at"])))
        FileUtil.write_file(DIR_O+title[:4]+"/"+title, FileUtil.process_content_new(content))
    return name,


def local_to_jianshu():
    last_file = FileUtil.get_last_file()
    (filepath, filename) = os.path.split(last_file)
    new_name = note_list()[0]['title']
    if not filename.startswith(new_name):
        try:
            content = replace_img_url(FileUtil.read_file(last_file))
        except Exception as e:
            #     抛出自定义异常
            FileUtil.notice_ding_error(str(e))
            raise Exception('图片简书上传失败！')
        article = create_article(filename.split(".")[0])
        write_content(content, str(article["id"]))
        link = "https://www.jianshu.com/p/" + article["slug"]
        FileUtil.write_file(file_path_online+filename[:4]+"/"+ filename, content)
        FileUtil.notice_ding(filename, content, link, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(article["content_updated_at"])))
        FileUtil.notice_wechat(link)
        return filename
    else:
        print("https://www.jianshu.com/p/" + note_list()[0]["slug"])
        return None

def dayone_to_local():
    article_path = ConfigUtils.get("icloud_path")
    if article_path is None:
        article_path = ConfigUtils.get("ali_path")
        from aligo import Aligo
        class CustomAligo(Aligo):
            """自定义 aligo """
            V3_FILE_DELETE = '/v3/file/delete'
            def delete_file(self, file_id: str, drive_id: str = None) -> bool:
                """删除文件"""
                drive_id = drive_id or self.default_drive_id
                response = self.post(self.V3_FILE_DELETE, body={
                    'drive_id': drive_id,
                    'file_id': file_id
                })
                return response.status_code == 204

        ali = CustomAligo()  # 第一次使用，会弹出二维码，供扫描登录
        fileList = ali.get_file_list("6538c5556b80c1ccbb4a40629284e0909be6e6fe")
        FileUtil.check_dir(article_path)
        ali.download_files(fileList, article_path)
        for e in fileList:
            ali.delete_file(file_id=e.file_id, drive_id=e.drive_id)

    FileUtil.check_dir(article_path)
    files = os.listdir(article_path)
    md_file = None
    jpg_file = None
    for file in files:
        if file.endswith(".txt"):
            md_file = os.path.join(article_path, file)
        if file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png"):
            jpg_file = os.path.join(article_path, file)
    if md_file is None:
        return None
    with open(md_file, 'r', encoding="utf-8") as file:
        now_day = ConfigUtils.get_now_day()
        year = now_day[:4]
        title = file.readline().replace("\n", "")
        if not title.startswith(year):
            title = '{}({})'.format(now_day, title)
        fileName = title + ".md"
        content = file.read()
        if jpg_file is not None:
            target_folder_2 = img_path + "/{}/".format(year)
            if not os.path.exists(target_folder_2):
                os.makedirs(target_folder_2)
            shutil.copy(jpg_file, os.path.join(target_folder_2, now_day + '.' + jpg_file.split(".")[1]))
            content = content  + "\n" + "![](../{}{})".format("../img/{}/".format(year), now_day + '.' + jpg_file.split(".")[1])

        if not os.path.exists(file_path + "/{}/".format(now_day[:4])):
            os.makedirs(file_path + "/{}/".format(now_day[:4]))
        content = prefix.format(ConfigUtils.get_now_str(), title, year, content)
        with open(file_path + '/{}/{}'.format(now_day[:4], fileName), 'w', encoding="utf-8") as file:
            file.write(content)
    shutil.rmtree(article_path)
    return md_file

def day_local_jian():
    try:
        dayone_to_local()
        time.sleep(10)
        try:
            fileName = local_to_jianshu()
        except Exception as e:
            FileUtil.notice_ding_error("简书异常")
            raise e
        time.sleep(3)
        locl_to_github()
        FileUtil.init_archives_readme()
        if fileName is not None:
            # FileUtil.init_readme()
            FileUtil.run_cmd("git add -A")
            FileUtil.run_cmd("git commit -m '{}'".format(fileName))
            FileUtil.run_cmd("git push -f")
    except Exception as e:
        print(e)
        FileUtil.notice_wechat(str(e))
        FileUtil.notice_ding_error(str(e))

def locl_to_github():
    last_file = FileUtil.get_last_file()
    (filepath, filename) = os.path.split(last_file)
    new_name = ConfigUtils.get("issue_title")
    if not filename.startswith(new_name):
        repo = GithubUtils.get_repo(ConfigUtils.get_local("git_token"), "mxz94/mxz_back")
        year = ConfigUtils.get_now_day()[:4]
        GithubUtils.create_issue(repo, src + r"/scripts/writenote/content/note/{}/{}".format(year,filename))
        ConfigUtils.set("issue_title", filename)

import random
import time

from paho.mqtt import client as mqtt_client

broker = 'p767a1ef.ala.cn-hangzhou.emqxsl.cn'
port = 8883
topic = 't/a'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# 如果 broker 需要鉴权，设置用户名密码
username = 'emqx'
password = 'emqx'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # Set CA certificate
    client.tls_set(ca_certs=src + r'\scripts\writenote/emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # FileUtil.notice_ding_error(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        day_local_jian()
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

def run_loop():
    interval = 3600
    while True:
        # 在此处执行您的任务
        print("执行定时任务...")
        day_local_jian()
        # 等待一段时间后再次执行任务
        time.sleep(interval)

if __name__ == '__main__':
    # t1 = Thread(target=run_loop)
    # t1.start()
    run()
    # FileUtil.init_archives_readme()
    # imgurl = upload_image(r"D:\mxz\mxz_back\src\content\img\2023\2023-12-07.jpeg")
    # print(imgurl)
    # FileUtil.download_image_file(imgurl, ConfigUtils.get_now_day())

    # repo = GithubUtils.get_repo(ConfigUtils.get_local("git_token"), "mxz94/mxz_back")
    # year = "2023"
    # GithubUtils.create_issue(repo, src + r"/scripts/writenote/content/note/{}/{}".format(year,year+"的展望.md"))