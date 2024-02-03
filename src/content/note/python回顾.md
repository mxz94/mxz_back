---
pubDatetime: 2024-02-02 10:11:47
title: python回顾
slug: python回顾
tags:
  - "计算机"
---


1. 切片 v[:2] 不包含 2  切片返回的是新list  
2. 函数接收参数 def cheeseshop(kind, *args, **keywords):   
cheeseshop("L", "A","B", shopkeeper="Michael Palin", client="John Cleese", sketch="Cheese Shop Sketch") args 接收元组   keywords 接收 dict
3. 格式化输出 f'年龄是{age}'
4. json.load() 和 json.dump  针对 file, 而loads 和dumps 针对的是字符串
5. 异常处理 try  except Exception as e:  raise 抛出异常
6. 类  @dataclass  类似c里面的struct
7. python 打包 pyinstaller --onefile your_script.py -i 11.ico
