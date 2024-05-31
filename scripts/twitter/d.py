import os

import requests

os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
headers = {
    'authority': 'api.tgx.one',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'if-none-match': 'W/"7af-lMN4qEWnHzebG+KCaE7YV4s/9WU"',
    'origin': 'https://tgx.one',
    'referer': 'https://tgx.one/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}

url = "https://twitter.com/i/status/1744411894956642591"
response = requests.get(
    'https://api.tgx.one/telegram/qTweet?url={}'.format(url),
    headers=headers,
)
def download_image_file(url, file):
    r = requests.get(url)
    with open(file, 'wb') as f:
        f.write(r.content)
        print(" # 写入DONE")
    return
import requests

def download_with_progress(url, file_path, callback):
    response = requests.get(url, stream=True)

    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0
    update_percentage = total_size * 0.05  # 5% 更新一次

    with open(file_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            downloaded_size += len(data)
            file.write(data)

            # 当下载量超过 5% 时，调用回调函数
            if downloaded_size >= update_percentage:
                callback(downloaded_size, total_size)
                update_percentage += total_size * 0.05

    # 确保最后一次调用回调函数
    callback(downloaded_size, total_size)

def progress_callback(downloaded_size, total_size):
    percent = (downloaded_size / total_size) * 100
    print(f"Downloaded: {downloaded_size} bytes / {total_size} bytes ({percent:.2f}%)")

url = "https://example.com/somefile.zip"
file_path = "downloaded_file.zip"


if (response.status_code == 200):
    dataList = response.json()["data"]["media"][0]["video_info"]["variants"]
    ret = max(dataList, key=lambda dic: dic.get('bitrate') if dic.get('bitrate') else 0)

    download_with_progress(ret["url"], "./sadasda23s.mp4", progress_callback)
    # download_with_progress(url, file_path, progress_callback)