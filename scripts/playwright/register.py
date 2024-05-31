from time import sleep

from playwright.sync_api import sync_playwright
account_list = ["mlx20240001",  "mlx20240002","mlx20240003","mlx20240004","mlx20240005", "mlx20240006","mlx20240007", "mlx20240008","mlx20240009", "mlx20240010","mlx20240011", "mlx20240012", "mlx20240013", "mlx20240014"]

with sync_playwright() as p:
    # p.chromium.launch(headless=False).new_context()
    # 启动持久上下文的context
    for ac_id in account_list:
        browser = p.chromium.launch_persistent_context(
            # 指定本机用户缓存地址
            user_data_dir=f"D:\chrome_userx\{ac_id}",
            # 接收下载事件
            accept_downloads=True,
            # 设置 GUI 模式
            headless=False,
            bypass_csp=True,
            slow_mo=1000,
            channel="msedge"
        )
        page = browser.pages[0]
        page.goto('https://cn.bing.com/search?q=demo')
        if not page.locator("#id_n").text_content().__eq__("杏争"):
            page.close();
            continue
        print(ac_id)
        page.pause()
        page.get_by_role("link", name="杏争").click()
        page.get_by_role("link", name="退出").click()
        page.get_by_role("button", name="登录").click()
        page.get_by_role("link", name="personal signin 使用个人帐户登录").click()
        page.get_by_test_id("i0116").click()
        page.pause()
        page.get_by_test_id("i0116").press("Control+a")
        page.get_by_test_id("i0116").fill(ac_id + "@outlook.com")
        page.get_by_role("button", name="下一个").click()
        page.get_by_test_id("i0118").press("Control+a")
        page.get_by_test_id("i0118").fill("qq741852")
        page.get_by_role("button", name="登录").click()
        page.get_by_label("保持登录状态?").click()
        page.pause()
        page.close()
