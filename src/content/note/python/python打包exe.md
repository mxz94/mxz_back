---
pubDatetime: 2024-01-18 17:58:28
title: python打包exe
slug: python打包exe
tags:
  - "工具"
  - "python"
---

# pyhon 打包工具

## pyinstaller
打包为一个文件 
pyinstaller --onefile your_script.py -i 11.ico


报错：
ImportError: DLL load failed while importing Win32Api

python pywin32_postinstall.py -install