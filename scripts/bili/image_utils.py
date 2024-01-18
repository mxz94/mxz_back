import requests



headers = {
    "Authorization" : "Bearer "+"149|TByGbpkb7ePEiIhEzyIm1f0hf6E3WRF2YkRChide",
    "Content-Type" : "multipart/form-data",
     "Accept" : "application/json"
}
files = {'file': ("成龙.jpg", open('D:\我的文档\Pictures\成龙.jpg', 'rb'), 'application/json')}
res = requests.post("https://www.freeimg.cn/api/v1/upload", files=files, headers=headers)
print(res.json()["data"]["links"]["url"])