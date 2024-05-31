import json
import os
import random
import time

import requests
from playwright.sync_api import sync_playwright

os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
def notice_ding_error(e: str):
    print(e)
    json_data = {
        "text": {
            "content":f"简书`{e}`"
        },
        "msgtype":"text"
    }

    response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=04ae95082327176ae45c70859b70b8f3043fa143c46d587236f6ddecce117a4f', json=json_data)
    print(response.json())
# "mlx20240002","mlx20240003","mlx20240004", "mlx20240005",,"mlx20240007","mlx20240008","mlx20240009", "mlx20240010", 1500
# hasrever  "mlx20240004",
# has abend "mlx20240002" "mlx20240001"
# has 换禁用  "mlx20240003", "mlx20240005""mlx20240007",
account_list = [ "mlx20240011", "mlx20240012", "mlx20240013", "mlx20240014","mlx20240015", "mlx20240016", "mlx20240017", "mlx20240018"]
account_list = ["mlx20240015", "mlx20240016", "mlx20240017", "mlx20240018"]
account_list = ["mlx20240008","mlx20240009", "mlx20240010"]
search_count = 35
search_list =[]
with open("./cy.json", "r", encoding="utf-8") as f:
    search_list = json.load(f)
numbers = list(range(1,len(search_list)))
with sync_playwright() as p:
    for account in account_list:
        # 启动持久上下文的context
        browser = p.chromium.launch_persistent_context(
            # 指定本机用户缓存地址
            user_data_dir=f"D:\chrome_userx\{account}",
            # 接收下载事件
            accept_downloads=True,
            # 设置 GUI 模式
            headless=False,
            bypass_csp=True,
            slow_mo=1000,
            channel="msedge"
        )
        page = browser.pages[0]
        id = ""
        page.goto('https://cn.bing.com/search?q='+search_list[random.choice(numbers)])
        page.pause()
        for i in range(1, search_count):
            page.goto('https://cn.bing.com/search?q='+search_list[random.choice(numbers)])
            page.get_by_placeholder("有问题尽管问我").click()
            page.get_by_placeholder("有问题尽管问我").press("Control+a")
            page.get_by_placeholder("有问题尽管问我").fill(search_list[random.choice(numbers)])
            page.get_by_placeholder("有问题尽管问我").press("Enter")
            sleep_time = random.uniform(15, 60)
            time.sleep(sleep_time)
            id = page.locator("#id_n").text_content()
            print(f"{account} == {id}完成第{i}次")
        page.close()
        notice_ding_error(f"{account} == {id}完成")
