import json
import random
import time

from playwright.sync_api import sync_playwright

ua = {
    "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 "
           "Safari/537.36",
    "app": "com.ss.android.ugc.aweme/110101 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; "
           "Cronet/TTNetVersion:b4d74d15 2020-04-23 QuicVersion:0144d358 2020-03-24)"
}
search_count = 30
search_list =[]
with open("./cy.json", "r", encoding="utf-8") as f:
    search_list = json.load(f)
numbers = list(range(1,len(search_list)))

def run():
    for i in range(1, 3):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                                              chromium_sandbox=False,
                                              ignore_default_args=["--enable-automation"],
                                        channel="msedge"
                                              )
            context = browser.new_context(storage_state=f"cookie{i}.json", user_agent=ua["web"])
            page = context.new_page()
            page.add_init_script(path="stealth.min.js")
            page.goto('https://cn.bing.com/search?q='+search_list[random.choice(numbers)])
            page.pause()
            for i in range(1, search_count):
                page.goto('https://cn.bing.com/search?q='+search_list[random.choice(numbers)])
                page.get_by_placeholder("有问题尽管问我").click()
                page.get_by_placeholder("有问题尽管问我").press("Control+a")
                page.get_by_placeholder("有问题尽管问我").fill(search_list[random.choice(numbers)])
                page.get_by_placeholder("有问题尽管问我").press("Enter")
                sleep_time = random.uniform(60, 120)
                time.sleep(sleep_time)
                id = page.locator("#id_n").text_content()
                print(f" {id}完成第{i}次")
            page.close()


if __name__ == '__main__':
    run()
    # scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    # scheduler.add_job(run, 'interval', minutes=30, misfire_grace_time=900)
    # scheduler.start()