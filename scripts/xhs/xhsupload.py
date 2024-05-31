import configparser
import json
import os
import random
import sqlite3
import threading
import time
from time import sleep

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from playwright.sync_api import sync_playwright
from xhs import XhsClient, SearchSortType

con2 = configparser.ConfigParser()

# 读取文件
con2.read("./config.ini", encoding='utf-8')

def check_in(number):
    with open("./issue.json", "r") as file:
        json_data = json.load(file)
    return number in json_data

def add_issue_id(id):
    with open("./issue.json", "r") as file:
        json_data = json.load(file)
    if id not in json_data:
        json_data.append(id)
    with open("./issue.json", "w") as file:
        json.dump(json_data, file)

def get(key:str, section='default'):
    items = con2.items(section) 	# 返回结果为元组
    items = dict(items)
    return items.get(key)
def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = r"./stealth.min.js"
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")

class XhsCli():

    @staticmethod
    def get_client(token):
        return XhsClient(token, sign=sign)
# with open("./demoxy2.txt", "r", encoding="utf8") as f:
#     demo = f.read()
def upload():
    print("aa")
    token = "a1=18899128b85l5n8twc100c9axk1spz7kx7ki6j47f50000247056; webId=15840f0fd45c7d6368c7ee14b82e26cf; gid=yYYjjyJYj2CKyYYjjyJYDWV4Y212IY9ESy88TWiSj0CTy328MUuWTK888J4W82K8qYKJ4W2f; gid.sign=0bbbu1JE19T6P9g0+QaoPEwa61M=; abRequestId=15840f0fd45c7d6368c7ee14b82e26cf; customerClientId=106623081685495; customer-sso-sid=662a3091300000000000000236fecfb13cc3fac0; x-user-id-creator.xiaohongshu.com=641a8696000000001201269c; access-token-creator.xiaohongshu.com=customer.ares.AT-9d03357963a244878db71c7cc47e9c20-3bbd6fac68ef4c31ac1714f64f361526; galaxy_creator_session_id=QyR5LR4JAEGjFkDoVU5WcMpmUpjMTxtHcC6H; galaxy.creator.beaker.session.id=1714040978116034641101; webBuild=4.14.1; acw_tc=73b5ac7e07ea491438c81cb424c853d1ef5d0b565dee8c69db50359506c1209d; web_session=040069b56ec5de1b76ca9b8918344bce588dff; unread={%22ub%22:%22662879780000000003020293%22%2C%22ue%22:%226628ed5400000000040186d8%22%2C%22uc%22:15}; xsecappid=ugc; websectiga=f3d8eaee8a8c63016320d94a1bd00562d516a5417bc43a032a80cbf70f07d5c0; sec_poison_id=96a3676d-8deb-4cea-9d60-1e58bdaca6dc"
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    client = XhsCli.get_client(token)
    file_list = os.listdir(r"E:\Program Files\telegram_media_downloader-2.2.0\downloads\回眸一笑\2023_01")
    for file_name in file_list:
        file_path = os.path.join(r"E:\Program Files\telegram_media_downloader-2.2.0\downloads\回眸一笑\2023_01", file_name)
        # 判断是否为文件
        if os.path.isfile(file_path):
            p,f = os.path.split(file_path)
            if f.endswith("mp4"):
                if check_in(f.split(' - ')[-1].split('.')[0]):
                    continue
                if os.path.getsize(file_path) > 5*1024*1024:
                    add_issue_id(f.split(' - ')[-1].split('.')[0])
                    continue
                data = client.create_video_note(file_path.split("\\")[-1].split("-")[0], file_path, file_path.split("\\")[-1].split("-")[0])
                print(data)
                add_issue_id(f.split(' - ')[-1].split('.')[0])
                break;

if __name__ == '__main__':
    while True:
        upload()
        sleep(100)