import os

import requests
from flask import Flask
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
headers = {
    'Content-Type': 'application/json',
}

params = {
    'key': 'AIzaSyA_D3B_6BAio2MGZc-asmjh3D_HGXPkLsU',
}

json_data = {
    'contents': [
        {
            'parts': [
                {
                    'text': '''
                    import os

headers = {
    'Content-Type': 'application/json',
}

params = {
    'key': 'AIzaSyA_D3B_6BAio2MGZc-asmjh3D_HGXPkLsU',
}

json_data = {
    'contents': [
        {
            'parts': [
                {
                    'text': '输入的文本',
                },
            ],
        },
    ],
}

response = requests.post(
    'https://gemini.mxz94.asia/v1beta/models/gemini-pro:generateContent',
    params=params,
    headers=headers,
    json=json_data,
)
print(response.json())
print(response.json()["candidates"][0]["content"]["parts"][0]["text"])

将这段代码转换为网页html  通过输入 js请求得到结果展示 不引入其他js 好看一点
                    ''',
                },
            ],
        },
    ],
}

response = requests.post(
    'https://gemini.mxz94.asia/v1beta/models/gemini-pro:generateContent',
    params=params,
    headers=headers,
    json=json_data,
)
print(response.json())
print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
