import os

import requests
from flask import Flask
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
headers = {
    'Content-Type': 'application/json',
}

params = {
    'key': 'AIzaSyBwJfDSPVDASV3MCn_wHb7tOkbRDUOqE1M',
}

json_data = {
    'contents': [
        {
            'parts': [
                {
                    'text': '美国首都？',
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
