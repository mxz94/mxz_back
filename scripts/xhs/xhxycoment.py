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
        cookie = "abRequestId=ec6c1792-722c-5cb7-8b4b-47b2fecc8ad5; webBuild=4.1.7; xsecappid=xhs-pc-web; a1=18dafed47adlfwxgyfmf087r7l5nrwkkr118gjgl950000362875; webId=0d55ea24de9ca41205cfa08f8a786327; websectiga=3633fe24d49c7dd0eb923edc8205740f10fdb18b25d424d2a2322c6196d2a4ad; sec_poison_id=5251cf97-7890-4197-9615-849032ae422d; gid=yYf0idf444FfyYf0idf4WyVk0f1iECkvi6i8y1jYWFW12Y28IFETTk888qKJYW280fW0SJ8q; web_session=040069b5800be046563ce19cfb374b26cc77d4; unread={%22ub%22:%2265adf24e00000000110033d3%22%2C%22ue%22:%2265aa6bf800000000100383be%22%2C%22uc%22:29}"
        return XhsClient(cookie, sign=sign)
with open("./demoxy.txt", "r", encoding="utf8") as f:
    demo = f.read()

if __name__ == '__main__':
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    client = XhsCli.get_client()
    for i in range(1, 10):
        data = client.get_note_by_keyword(keyword="", sort=SearchSortType.LATEST, page=i)
        items = data["items"]
        # items = client.get_home_feed(xhs.FeedType.RECOMMEND)["items"]
        for item in items:
            try:
                # title = item["note_card"]["display_title"]
                id = item["id"]
                for get_note_comment in client.get_note_comments(note_id=id):
                    content = get_note_comment["content"]
                    if "content" in content:
                        cid = get_note_comment["id"]
                        client.like_comment(id, cid)
            except Exception as e:
                print("error")
                pass