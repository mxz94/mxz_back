import calendar
import json
import re
import time
from datetime import datetime

import requests

from main import get_article_attrs
from scripts.utils.file_utils import FileUtils

if __name__ == '__main__':
    mid = 13
    list = FileUtils.read_all_file(r'D:\mxz\mxz_back\src\content\note')
    for item in list:
        data = get_article_attrs(item);
        data.content = data.content.replace("../../../public", "https://blog.malanxi.top")
        img = None
        markdown_image_pattern = re.compile(r'!\[(.*?)\]\(([^)]+)\)')
        for match in markdown_image_pattern.finditer(data.content):
            alt_text = match.group(1)  # 获取 alt 文本
            img = match.group(2)  # 获取图片的 URL
            break
        try:
            dt = datetime.strptime(data.pubDatetime, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            dt = datetime.strptime(data.pubDatetime, '%Y-%m-%dT%H:%M:%SZ')
        timestamp = calendar.timegm(dt.timetuple())
        data = {
            "title": data.title,
            "str_value": img,
            "text": data.content,
            "mid": mid,
            "created": timestamp
        }
        url = "https://pblog.malanxi.top/insert.php"
        response = requests.post(url, headers={"Content-Type": "application/json; charset=utf-8"}, data=json.dumps(data).encode('utf-8'))
        print(response.text)