import json

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)

cors = CORS(app)
GEMINI_API_KEY = "AIzaSyA_D3B_6BAio2MGZc-asmjh3D_HGXPkLsU"
GEMINI_API_URL = "https://gemini.mxz94.asia/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    # 获取请求中的 JSON 数据
    request_data = request.json

    # 从 JSON 数据中提取所需的字段
    model = request_data.get('model', '')
    messages = request_data.get('messages', [])
    temperature = request_data.get('temperature', 1.0)
    stream = request_data.get('stream', False)

    # 打印提取到的数据（你可以根据实际需要进行处理）

    # 构建请求给 Gemini API
    gemini_request_data = {
        "contents": [
            {
                "parts": [{"text": messages[0]["content"]}]
            }
        ]
    }

    headers = {'Content-Type': 'application/json'}
    gemini_response = requests.post(GEMINI_API_URL, json=gemini_request_data, headers=headers)
    data = gemini_response.json()["candidates"][0]["content"]["parts"][0]["text"].replace("```json", "").replace("```", "")
    # 获取 Gemini API 的响应
    response_data = {
        "id": "79fb180d21694513",  # 从 Gemini API 响应中获取的值
        "object": "chat.completion.chunk",
        "created": 3705525,  # 从 Gemini API 响应中获取的值
        "model": "yi-34b-chat",  # 从 Gemini API 响应中获取的值
        "choices": [{"delta":{"role":"assistant","content":""},"index":0,"finish_reason":"stop", "message":{"content":data}}],
        "content": data,
        "usage": {"completion_tokens":27,"prompt_tokens":14,"total_tokens":41},
        "lastOne": True
    }
    print(json.loads(data))
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)