import os
from time import sleep

from playwright.sync_api import sync_playwright
from xhs import XhsClient


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


list = ["6113d62b000000000101f735"]
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
cookie = "a1=18899128b85l5n8twc100c9axk1spz7kx7ki6j47f50000247056; webId=15840f0fd45c7d6368c7ee14b82e26cf; gid=yYYjjyJYj2CKyYYjjyJYDWV4Y212IY9ESy88TWiSj0CTy328MUuWTK888J4W82K8qYKJ4W2f; gid.sign=0bbbu1JE19T6P9g0+QaoPEwa61M=; abRequestId=15840f0fd45c7d6368c7ee14b82e26cf; customerClientId=106623081685495; x-user-id-creator.xiaohongshu.com=641a8696000000001201269c; acw_tc=2cb7f56c2db1ab1178d88ec9349ae7716ee5039359fb98f99b352f7b4639fe27; webBuild=4.17.2; web_session=040069b56ec5de1b76caaafa64344b95b6d93d; unread={%22ub%22:%22665094320000000015013592%22%2C%22ue%22:%226650b30300000000050049dc%22%2C%22uc%22:33}; websectiga=82e85efc5500b609ac1166aaf086ff8aa4261153a448ef0be5b17417e4512f28; sec_poison_id=3c5235c3-dd1b-4e5d-9399-6fd0045f6e9a; customer-sso-sid=68c51737287096782851612473a37ceec4330635; access-token-creator.xiaohongshu.com=customer.creator.AT-68c5173728709678285161271fr2elxhpukyeinu; galaxy_creator_session_id=i33NiON6p9INMejwq0rnzRlxnb7YKOiOZ9PR; galaxy.creator.beaker.session.id=1716630293620025046551; xsecappid=ugc"
cl = XhsCli.get_client(cookie)
# list = cl.get_user_notes(user_id="60bc119a0000000001004741")
# data = cl.get_note_by_keyword("jvm")
# beauty_print(data)
# data= cl.get_note_by_keyword("三亚", page=1, page_size=20)
# for item in data["items"]:
#     print(item)
# print(cl.save_files_from_note_id(item["id"], dir_path="D:/xhs"))
# print(cl.get_user_info("64ca3f22000000000e024ea8"))
# list = cl.get_user_all_notes(user_id="64ca3f22000000000e024ea8")
# print(cl.save_note_by_id("657fa6e5000000003c011acf", dir_path="D:/xhs"))
for item in list:
    cl.save_user_all_notes(user_id=item, dir_path="D:/xhs2", crawl_interval = 0)

# key = ""
# download_by_search
# cl.save_search_notes(key= "三亚", dir_path="D:/xhs", crawl_interval = 0)