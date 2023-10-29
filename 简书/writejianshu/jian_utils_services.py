import configparser
import datetime
import os
import re
import shutil
import time

import html2text
import qiniu
import requests

file = 'D:\mxz\mxz_back\简书\writejianshu\config.ini'

# 创建配置文件对象
con = configparser.ConfigParser()

# 读取文件
con.read(file, encoding='utf-8')


class ConfigUtils:
    @staticmethod
    def get_now_day():
        return str(datetime.date.today())
    @staticmethod
    def get(key:str, section='default'):
        items = con.items(section) 	# 返回结果为元组
        items = dict(items)
        return items.get(key)

IMG_DIR = "../img"
IMG_DIR_2 = r"D:\mxz\mxz_back\简书/img"
directory_path = r"D:\mxz\mxz_back\简书/note_o"
dd = '''
<details {}><summary>{}</summary>
<p>

{}

</p>
</details>
'''
class FileUtil:
    @staticmethod
    def check_dir(dir:str):
        if not os.path.exists(dir):
            os.makedirs(dir)
    @staticmethod
    def get_last_file():
        year = ConfigUtils.get_now_day()[:4]
        folder_path = directory_path + "/" + year
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
    def download_image_file(url):
        r = requests.get(url)
        file = os.path.join(IMG_DIR_2, os.path.basename(url))
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

DIR= r'D:\mxz\mxz_back\简书/note/'
DIR_O= r'D:\mxz\mxz_back\简书/note_o/'

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
    ret, info = qiniu.put_file(data["token"], data["key"], r"D:\mxz\mxz_back\简书/img/{}/{}".format(filename[:4], filename))
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
        content = replace_img_url(FileUtil.read_file(last_file))
        article = create_article(filename.split(".")[0])
        write_content(content, str(article["id"]))
        link = "https://www.jianshu.com/p/" + article["slug"]
        FileUtil.write_file(DIR+filename[:4]+"/"+ filename, content)
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
        if file.endswith(".jpeg"):
            jpg_file = os.path.join(article_path, file)
    if md_file is None:
        return None
    with open(md_file, 'r', encoding="utf-8") as file:
        now_day = ConfigUtils.get_now_day()
        year = now_day[:4]
        fileName = file.readline().replace("\n", "")
        if not fileName.startswith(year):
            fileName = '{}({})'.format(now_day, fileName)
        fileName = fileName + ".md"
        content = file.read()
        if jpg_file is not None:
            target_folder = "../img/{}/".format(year)
            target_folder_2 = r"D:\mxz\mxz_back\简书/img/{}/".format(year)
            if not os.path.exists(target_folder_2):
                os.makedirs(target_folder_2)
            shutil.copy(jpg_file, os.path.join(target_folder_2, now_day + '.jpeg'))
            content = content  + "\n" + "![](../{}{})".format(target_folder, now_day + '.jpeg')

        if not os.path.exists(r"D:\mxz\mxz_back\简书/note_o/{}/".format(now_day[:4])):
            os.makedirs(r"D:\mxz\mxz_back\简书/note_o/{}/".format(now_day[:4]))

        with open(r'D:\mxz\mxz_back\简书/note_o/{}/{}'.format(now_day[:4], fileName), 'w', encoding="utf-8") as file:
            file.write(content)
    shutil.rmtree(article_path)
    return md_file

def day_local_jian():
    try:
        dayone_to_local()
        fileName = local_to_jianshu()
        if fileName is not None:
            FileUtil.init_readme()
            FileUtil.run_cmd("git add -A")
            FileUtil.run_cmd("git commit -m '{}'".format(fileName))
            FileUtil.run_cmd("git push -f")
    except Exception as e:
        print(e)
        FileUtil.notice_wechat(str(e))
        FileUtil.notice_ding_error(str(e))


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
    client.tls_set(ca_certs=r'D:\mxz\mxz_back\简书\writejianshu/emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        FileUtil.notice_ding_error(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
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
    run()