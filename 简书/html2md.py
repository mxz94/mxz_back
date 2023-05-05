import glob
import os

import html2text
import sys

DIR = "./files"
DIR_NEW = "./files"
args = sys.argv
if len(args) == 2:
    DIR_NEW = DIR = args[1]
if len (args) == 3:
    DIR = args[1]
    DIR_NEW = args[2]

if __name__ == '__main__':
    # 读取指定文件夹下指定类型html
    file_pattern = os.path.join(DIR, "*.html")
    files = glob.glob(file_pattern)
    for file in files:
        with open(file, "r",  encoding='utf-8') as f:
            content = f.read()
        md = html2text.html2text(content)
        new_file = file.replace(DIR, DIR_NEW).replace(".html", ".md")
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(md)
        os.remove(file)
