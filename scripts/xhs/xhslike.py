import configparser
import os
import random
import sqlite3
import time
from time import sleep
word = ("洛阳相亲"
        "")
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

if __name__ == '__main__':
    token = "abRequestId=4548c8e1-c7f9-53b1-b573-98b591e45783; webBuild=4.85.1; xsecappid=xhs-pc-web; a1=19a8048f0f18nrijvv4c8f1v6ynk5n09sdvj9epdn50000159736; webId=36b58831d866d742d7cd4207a8ecd303; acw_tc=0a4acac317630888529021589e41896f01bfb3c8d00b39520d54444ad7c601; websectiga=7750c37de43b7be9de8ed9ff8ea0e576519e8cd2157322eb972ecb429a7735d4; sec_poison_id=b1db3be8-c833-4595-b9c6-0a1a649765e6; gid=yj0Y84jy0JMSyj0Y84Yi8fdUiyYIF3Vhh4SYhfIiyhKvIV28T2I8jj888y2jWqK8fjjKWfjd; web_session=040069b4a5e736438e5e65d2233b4b45944720; unread={%22ub%22:%2268f834fe000000000301abf8%22%2C%22ue%22:%22690d9a150000000004005d89%22%2C%22uc%22:29}; loadts=1763088946894"
    keyword = word
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
                client.like_note(note_id)
                s = s  + 1
                print(title + ": " +str(s))
                sleep_time = random.uniform(20, 30)
                time.sleep(sleep_time)
            except Exception as e:
                print(e)
                pass
