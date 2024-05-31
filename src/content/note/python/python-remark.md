---
pubDatetime: 2024-02-02 10:11:47
title: python-remark
slug: python-remark
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
8. pip install --upgrade package_name 升级包
9. pip 找不到时， 可以用 python -m pip  安装太慢  -i https://pypi.douban.com/simple 或修改 
   `或者修改 Users/pip/pip.ini
   [global]
   index-url = https://pypi.tuna.tsinghua.edu.cn/simple
   [install]
   trusted-host=mirrors.aliyun.com`
10. 生成项目依赖包 pip freeze > requirements.txt 生成依赖资源文件 环境所有包全都导出了
11. 方法内修改全局变量必须在方法内用global 声明
12. 三目运算符 a if b > 0 else c 
13. [l.name for l in lines]