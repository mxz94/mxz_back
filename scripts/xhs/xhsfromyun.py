import configparser
import os
import random
import sqlite3
import time
from time import sleep

import requests
from playwright.sync_api import sync_playwright
from xhs import XhsClient, SearchSortType

con2 = configparser.ConfigParser()
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
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

con = sqlite3.connect("xhs.db")

def ask_gemmin(content):
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': 'AIzaSyBwJfDSPVDASV3MCn_wHb7tOkbRDUOqE1M',
    }

    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': content,
                    },
                ],
            },
        ],
    }

    response = requests.post(
        'https://gemini.malanxi.top/v1beta/models/gemini-pro:generateContent',
        params=params,
        headers=headers,
        json=json_data,
    )
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]
def add(user_id, note_id, title, user_name):
    try:
        sql = f'replace INTO "xhs" ("user_id", "note_id", "title", "user_name") VALUES ("{user_id}", "{note_id}", "{title}", "{user_name}");'
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
    except Exception as e:
        print(e)

def count(user_id, note_id):
    try:
        cur = con.cursor()
        cur.execute("SELECT count(1) from xhs where user_id ='"+user_id+"' and note_id = '"+note_id+"'")
        list = cur.fetchall()
        return list[0][0] != 0
    except Exception as e:
        print(e)
def select_list(table, wsql):
    try:
        cur = con.cursor()
        cur.execute("SELECT * from "+table+" where "+ wsql+"")
        list = cur.fetchall()
        return list
    except Exception as e:
        print(e)

def select(table, wsql):
    try:
        cur = con.cursor()
        cur.execute("SELECT * from "+table+" where "+ wsql+"")
        list = cur.fetchall()
        return list[0]
    except Exception as e:
        print(e)
# xq
xq = 1
ly = 2
user_name = "maback"
type = xq
emoji_list = ["😀","😁","😂","🤣","😄","😅","😆","😎","🤑","🧏","👨"]
if __name__ == '__main__':
    data = select("user", "name = '"+ user_name+"' and type = '" + str(type) + "'")
    if data == None:
        print("未找到用户")
    token = data[0]
    keyword = data[1]
    comment = data[2]
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    client = XhsCli.get_client(token)
    user_id = client.get_self_info2()["user_id"]
    s = 0
    for i in range(1, 16):
        data = client.get_note_by_keyword(keyword=keyword, sort=SearchSortType.GENERAL, page=i)
        items = data["items"]
        for item in items:
            try:
                note_id = item["id"]
                try:
                    title = item["note_card"]["display_title"]
                except Exception as e:
                    title = ""
                model_type = item["model_type"]
                if model_type != "note":
                    continue
                if (count(user_id, note_id)):
                    continue
                client.comment_note(note_id, comment+ emoji_list[random.randint(0, len(emoji_list) - 1)])
                add(user_id, note_id, title, user_name)
                s = s  + 1
                print(title + ": " +str(s))
                sleep_time = random.uniform(20, 30)
                time.sleep(sleep_time)
            except Exception as e:
                print(e)
                pass
