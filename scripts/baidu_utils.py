import os
import pandas as pd
import requests

from map_utils import bd09_to_wgs84

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

def tr(x, y):
    import requests

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.lddgo.net',
        'priority': 'u=1, i',
        'referer': 'https://www.lddgo.net/',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    }

    json_data = {
        'from': 'bd09',
        'coordinateList': [
            {
                'sourceLng': x,
                'sourceLat': y,
            },
        ],
    }

    response = requests.post('https://openapi.lddgo.net/base/gtool/api/v1/CoordinateTransform', headers=headers, json=json_data)
    print(response.json())
    data = response.json()["data"]["coordinateList"][0]
    return data["wLng"], data["wLat"]

ak = "M7olmu7pXDVznsM1CdEXTG66B4hl4jWq"
url = f"https://api.map.baidu.com/directionlite/v1/riding?origin=34.601574,112.521424&destination=34.620594,112.460767&ak={ak}"

payload = {}
headers = {
    'Accept': 'application/json',
    'x-api-key': '0EA0aUMeeFtAlNA9naNwjH1ECpZfTiCfUVMNF5A'
}


response = requests.request("GET", url, headers=headers, data=payload)
data = {
    'X': [],
    'Y': []
}

for item in response.json()["result"]['routes'][0]["steps"]:
    start_location = item["start_location"]
    end_location = item["end_location"]
    da = bd09_to_wgs84(float(start_location['lng']), float(start_location['lat']))
    da1 = bd09_to_wgs84(float(end_location['lng']), float(end_location['lat']))
    lng,lat = da[0], da[1]
    lngg,latt = da1[0], da1[1]
    data["X"].append(lng)
    data["X"].append(lngg)
    data["Y"].append(lat)
    data["Y"].append(latt)

df = pd.DataFrame(data)

# 写入 Excel 文件
df.to_csv('example_pandas.csv', index=False, encoding='utf-8')
print("数据已写入 example_pandas.csv")