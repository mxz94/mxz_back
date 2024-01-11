import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer soulteary',
}

json_data = {
    'model': 'gpt-4',
    'messages': [
        {
            'role': 'user',
            'content': 'Hello.',
        },
    ],
    'temperature': 0.2,
    'stream': True,
}

response = requests.post('http://127.0.0.1:8080/v1/chat/completions', headers=headers, json=json_data)
print(response.text)