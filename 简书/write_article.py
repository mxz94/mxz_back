import os

from 简书.writejianshu.jian_utils import FileUtil

prefix = """---
pubDatetime: {}T00:00:00Z
title: {}
tags:
  - "{}"
---

{}
"""
for e in os.listdir("note_o"):
    for file in os.listdir(os.path.join("note_o", e)):
        with open(os.path.join("note_o", e, file), "r", encoding="utf8") as f:
            title = file[:-3]
            date = file[:10]
            if title == date:
                title = '"{}"'.format(title)
                print(title)
            tags = file[:4]
            content = f.read()
            if date.endswith("("):
                print(date)
            FileUtil.check_dir(os.path.join("blog", e))
            with open(os.path.join("blog", e, file), "w", encoding="utf8") as f2:
                f2.write(prefix.format(date, title, tags, content))