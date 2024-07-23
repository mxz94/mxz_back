import os

import psycopg2
import requests
from psycopg2 import sql

# 数据库连接配置
DB_HOST = "127.0.0.1"
DB_NAME = "immich"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_PORT = "5432"  # 通常是5432

def connect_to_db():
    try:
        # 建立数据库连接
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        print("连接成功")
        return conn
    except Exception as e:
        print(f"连接失败: {e}")
        return None

def read_data(conn):
    try:
        # 创建一个游标对象
        cur = conn.cursor()
        # 执行SQL查询
        cur.execute("SELECT * FROM exif")
        # 获取所有结果
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print(f"读取数据失败: {e}")

def update_data(conn, city,state,description, assetId):
    try:
        # 创建一个游标对象
        cur = conn.cursor()
        # 执行SQL更新
        cur.execute(
            sql.SQL("UPDATE public.exif SET city = %s, state =%s, description=%s WHERE public.assetId = %s"),
            [city,state,description, assetId]
        )
        # 提交更改
        conn.commit()
        cur.close()
        print("数据更新成功")
    except Exception as e:
        print(f"数据更新失败: {e}")
        conn.rollback()

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

def main():
    # 连接到数据库
    conn = connect_to_db()
    if conn:
        # 读取数据
        list = read_data(conn)
        for e in list:
            print(e)
            print(e[13])
            print(e[14])
            location = f'{e[14]},{e[13]}'
            address_info = gps_to_address(api_key, location, extensions='base', roadlevel=1)
            update_data(conn,address_info["addressComponent"]["city"] ,address_info["addressComponent"]["province"],address_info["formatted_address"], e[1])
        # 关闭数据库连接
        conn.close()

if __name__ == "__main__":
    main()