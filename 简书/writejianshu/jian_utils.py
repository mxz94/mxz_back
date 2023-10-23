import os
import re
import sys

import html2text
import qiniu
import requests

import datetime
import os
import re

import requests

proxy = '127.0.0.1:7890'

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

folder_path = "../note_o/2023"
IMG_DIR = "../img"
directory_path = "../note_o"
dd = '''
<details {}><summary>{}</summary>
<p>

{}

</p>
</details>
'''
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
    def download_image_file(url):
        r = requests.get(url)
        file = os.path.join(IMG_DIR, os.path.basename(url))
        with open(file, 'wb') as f:
            f.write(r.content)
            print(" # 写入DONE")
        return

    @staticmethod
    def init_readme(fileName = "README.md" , pg = "note_o"):
        FileUtil.init_o_readme("README.md", "note_o")
        FileUtil.init_o_readme("README_JIAN.md", "note")
        FileUtil.init_oline_readme()

    @staticmethod
    def init_o_readme(fileName = "README.md" , pg = "note_o"):
        # 使用os.listdir()获取目录下所有文件和文件夹的列表
        file_names = os.listdir(directory_path)
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
        with open("../"+ fileName, 'w', encoding='utf-8') as file:
            open2 = "open"
            for key, value in re_s:
                content = ""
                for item in value:
                    content += item + "<br>\n"
                    # file.write(item + "<br>\n")
                file.write(dd.format(open2,key, content))
                open2 = ""

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
            with open("../"+ fileName, 'w', encoding='utf-8') as file:
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

DIR= '../note/'
DIR_O= '../note_o/'

cookies = {
    '_ga': 'GA1.2.737969924.1685589635',
    '_ga_Y1EKTCT110': 'GS1.2.1696579475.16.1.1696579533.0.0.0',
    'Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068': '1695798359,1696579447,1697534452',
    'Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068': '1697534452',
    'locale': 'zh-CN',
    'gdt_fp': 'f3a8181abe74958c45d1fb42ee9b7fe0',
    'mobile-index-modal': '1',
    'read_mode': 'day',
    'default_font': 'font2',
    'remember_user_token': 'W1s2OTA0MzE1XSwiJDJhJDEwJDRjbkxQOE9iSHZGeDRyT3hzMnpSek8iLCIxNjk3NjEzNTc0LjI3NTE4MjUiXQ%3D%3D--32887858f7a41cc65b26bd9c99984e6444b3b376',
    '_m7e_session_core': 'ccfcfc3e76cad18f647db7009fcaf380',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218866f985e0100b-07b74986a20881-26031a51-3686400-18866f985e111c7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218866f985e0100b-07b74986a20881-26031a51-3686400-18866f985e111c7%22%7D',
}
headers = {
    'Host': 'www.jianshu.com',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'accept': 'application/json',
    'content-type': 'application/json; charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.jianshu.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.jianshu.com/writer',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

def upload_image(file:str):
    (filepath, filename) = os.path.split(file)
    print(filename)
    params = {
        'filename': filename,
    }
    response = requests.get('https://www.jianshu.com/upload_images/token.json', params=params, cookies=cookies, headers=headers)
    data = response.json()
    ret, info = qiniu.put_file(data["token"], data["key"], "../img/{}".format(filename))
    return ret['url']


def replace_img_url(content):
    pattern = r'\((.*?)\)'
    matchs = re.findall(pattern, content)
    for img_path in matchs:
        imgurl = upload_image(img_path)
        print(imgurl)
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
    content = replace_img_url(content)
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
def notice_wechat(title: str):
    response = requests.get('https://sctapi.ftqq.com/SCT142512TIZeFu7Dj22drBfQgwT0KPIdI.send?title={}'.format(title), proxies=proxies)
    return response.json()

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
        FileUtil.write_file(DIR+title[:4]+"/"+ title, FileUtil.process_content_new(content, True))
        FileUtil.write_file(DIR_O+title[:4]+"/"+title, FileUtil.process_content_new(content))
    return name


def local_to_jianshu():
    last_file = FileUtil.get_last_file()
    (filepath, filename) = os.path.split(last_file)
    new_name = note_list()[0]['title']
    if not filename.startswith(new_name):
        content = FileUtil.read_file(last_file)
        article = create_article(filename)
        write_content(content, str(article["id"]))
        print("https://www.jianshu.com/p/" + article["slug"])
    else:
        print("https://www.jianshu.com/p/" + note_list()[0]["slug"])
    return filename

if __name__ == '__main__':
    # print("1  jianshu_to_local")
    # print("2  local_to_jianshu")
    # age = input("select sync type： 1  jianshu_to_local (default) 2  local_to_jianshu\n")
    # if age == '' or age == '1':
    #     filename = jianshu_to_local()
    # else:
    #     filename = local_to_jianshu()
    try:
        filename = jianshu_to_local()
        FileUtil.init_readme()
        FileUtil.run_cmd("git add -A")
        FileUtil.run_cmd("git commit -m '{}'".format(filename))
        FileUtil.run_cmd("git push -f")
        notice_wechat(filename)
    except Exception as e:
        print(e)
        notice_wechat("str(e)")

