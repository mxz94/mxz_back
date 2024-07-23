import os

import requests

def gps_to_address(api_key, location, poitype=None, radius=1, extensions='base', roadlevel=None, output='JSON', callback=None, homeorcorp=None):
    # 构造请求URL
    url = f"https://restapi.amap.com/v3/geocode/regeo"

    # 构造请求参数
    params = {
        'key': api_key,
        'location': location,
        'radius': radius,
        'extensions': extensions,
        'output': output
    }

    # 添加可选参数
    if poitype:
        params['poitype'] = poitype
    if roadlevel:
        params['roadlevel'] = roadlevel
    if callback:
        params['callback'] = callback
    if homeorcorp:
        params['homeorcorp'] = homeorcorp

    # 发送请求
    response = requests.get(url, params=params)

    # 解析响应
    if response.status_code == 200:
        result = response.json()
        if result['status'] == '1':
            return result['regeocode']
        else:
            return "逆地理编码失败：" + result['info']
    else:
        return "HTTP请求失败：" + str(response.status_code)
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
# 示例使用
api_key = ""
location = "112.478775,34.6813194444444"  # 经度在前，纬度在后
address_info = gps_to_address(api_key, location, extensions='base', roadlevel=1)
print(address_info["formatted_address"])
print(address_info["addressComponent"])