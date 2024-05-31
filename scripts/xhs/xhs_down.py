import os

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


list = ["609f89f20000000001003ce2"]
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
cl = XhsCli.get_client()
cl.get
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
if __name__ == '__main__':
    cl.create_image_note_by_path(r"D:\xhs")
# key = ""
# download_by_search
# cl.save_search_notes(key= "三亚", dir_path="D:/xhs", crawl_interval = 0)