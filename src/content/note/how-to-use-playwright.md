---
title: how-to-use-playwright
pubDatetime: 2024-04-13 10:23:00
slug: how-to-use-playwright
tags:
  - "工具"
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

4. docker 部署
Dockerfile 文件
```
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 配置阿里云和清华镜像源
RUN echo \
    "deb http://mirrors.aliyun.com/debian/ bullseye main contrib non-free\n" \
    "deb http://mirrors.aliyun.com/debian/ bullseye-updates main contrib non-free\n" \
    "deb http://mirrors.aliyun.com/debian-security bullseye-security main contrib non-free\n" \
    "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free\n" \
    "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free\n" \
    "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free" \
    > /etc/apt/sources.list

# 安装 Playwright 依赖
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --fix-missing \
    libwebkit2gtk-4.0-37 \
    libgtk-3-0 \
    libgbm1 \
    libxcb-render0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libexpat1 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 && \
    rm -rf /var/lib/apt/lists/*

# 升级 pip 并安装 playwright
RUN python -m pip install --upgrade pip && \
    pip install playwright && \
    playwright install chrome

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 默认命令
CMD ["bash"]
```

```
# 构建
docker build -t my-playwright-app .

# 运行
docker run -it my-playwright-app
```
