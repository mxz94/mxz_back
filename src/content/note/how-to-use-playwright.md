---
title: how-to-use-playwright
pubDatetime: 2024-04-13
tags:
  - 工具
---

# 一. 什么是playwright，为什么要用它

playwright  自动化测试工具

对比selenium， 不需要安装各种驱动， 之前每次浏览器更新都需要找最新的driver， 支持各种主流语言

# 二. 安装使用

```bash
pip install playwright
```

```
playwright install
```

1. 录制脚本

```bash
python -m playwright codegen --target python -o 'my.py' -b chromium https://github.com/

playwright codegen --save-storage=auth.json  # 存储到本地
playwright open --load-storage=auth.json my.web.app  # 打开存储
playwright codegen --load-storage=auth.json my.web.app # 使用存储运行生成代码（保持认证状态）
```

2. 半途选择record 录制

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # p.chromium.launch(headless=False).new_context()
    # 启动持久上下文的context
    browser = p.chromium.launch_persistent_context(
        # 指定本机用户缓存地址
        user_data_dir=f"D:\chrome_userx\yoyo",
        # 接收下载事件
        accept_downloads=True,
        # 设置 GUI 模式
        headless=False,
        bypass_csp=True,
        slow_mo=1000,
        channel="msedge"
    )
    page = browser.pages[0]
    page.goto('https://github.com/')
    page.pause()
    # 设置最大等待超时时间（超过该时间则会报错 ）
    page.wait_for_timeout(3000)
```

3. 常用方法

```
page.get_by_placeholder("请输入手机号/邮箱").click()
page.get_by_placeholder("请输入手机号/邮箱").fill("")
page.get_by_role("button", name="Delete issue").click()
page.locator("text=Delete this issue").click()
page.get_by_test_id()
```
