import os

from scripts.writejianshu2.jian_utils_services import FileUtil

prefix = """---
pubDatetime: {}T00:00:00Z
title: {}
tags:
  - "{}"
---

{}
"""
for e in os.listdir(r"D:\mxz\mxz_back\src\content\blog"):
    for file in os.listdir(os.path.join(r"D:\mxz\mxz_back\src\content\blog", e)):
        with open(os.path.join(r"D:\mxz\mxz_back\src\content\blog", e, file), "r", encoding="utf8") as f:
            title = file[:-3]
            date = file[:10]
            if title == date:
                title = '"{}"'.format(title)
                print(title)
            tags = file[:4]
            content = f.read()
            with open(os.path.join(r"D:\mxz\mxz_back\src\content\blog", e, file), "w", encoding="utf8") as f2:
                f2.write(prefix.format(date, title, tags, content))