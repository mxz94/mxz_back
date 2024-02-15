import datetime
import json
import os
from time import sleep

import xhs
from xhs import XhsClient, DataFetchError, help, SearchSortType
from playwright.sync_api import sync_playwright


def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = r"D:\docker\xhs\stealth.min.js"
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
    def get_client():
        cookie = "a1=18899128b85l5n8twc100c9axk1spz7kx7ki6j47f50000247056; webId=15840f0fd45c7d6368c7ee14b82e26cf; gid=yYYjjyJYj2CKyYYjjyJYDWV4Y212IY9ESy88TWiSj0CTy328MUuWTK888J4W82K8qYKJ4W2f; gid.sign=0bbbu1JE19T6P9g0+QaoPEwa61M=; abRequestId=15840f0fd45c7d6368c7ee14b82e26cf; xsecappid=xhs-pc-web; webBuild=4.1.6; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=29db9b00-877f-4716-a1d0-6d0c6241d09d; web_session=040069b56ec5de1b76ca8904f5374b21200815; cacheId=191a3243-0ee6-4534-9fb2-add2a2cba38e; unread={%22ub%22:%2265bd0c410000000007029c28%22%2C%22ue%22:%2265bf858c000000002c0384af%22%2C%22uc%22:24}"
        return XhsClient(cookie, sign=sign)
with open("./demo.txt", "r", encoding="utf8") as f:
    demo = f.read()

if __name__ == '__main__':
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    client = XhsCli.get_client()
    for i in range(1, 6):
        data = client.get_note_by_keyword(keyword="", sort=SearchSortType.GENERAL, page=i)
        items = data["items"]
        # items = client.get_home_feed(xhs.FeedType.RECOMMEND)["items"]
        for item in items:
            try:
                # title = item["note_card"]["display_title"]
                id = item["id"]
                client.comment_note(id, demo)
            except Exception as e:
                print("error")
                pass