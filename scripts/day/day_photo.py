import datetime
import os

import cv2
import qiniu
import requests

now = datetime.datetime.now()
year = now.strftime("%Y")
name = now.strftime("%Y-%m-%d")


@staticmethod
def notice_ding(title, content):
    json_data = {"title":title,"content":content,}
    response = requests.post('https://xizhi.qqoq.net/XZb02fde849963687f64a219eafba83a6b.send', json=json_data)
    print(response.json())

dir = r'D:\Administrator\Pictures\profile\{}'.format(year)
filename = dir+ r'\{}.jpg'.format(name)

cookies = {
    '_ga': 'GA1.2.316202546.1695480391',
    'Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068': '1699181179',
    '_ga_Y1EKTCT110': 'GS1.2.1699183942.3.0.1699183942.0.0.0',
    'read_mode': 'day',
    'default_font': 'font2',
    'locale': 'zh-CN',
    'remember_user_token': 'W1s2OTA0MzE1XSwiJDJhJDEwJDRjbkxQOE9iSHZGeDRyT3hzMnpSek8iLCIxNzAzNjgzNjYzLjY4NDU5MSJd--6480768a59c698eb18fcb1917b1866e61a507a9c',
    'web_login_version': 'MTcwMzY4MzY2Mw%3D%3D--f26ac4e6d80ee0411350625c3b2559e1ea257838',
    '_m7e_session_core': 'd95f9823abfb793f9cbafa126b20a384',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%226904315%22%2C%22first_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218ac281a32a86c-0f28170cbca7b1-26031e51-1382400-18ac281a32ba28%22%7D',
}

headers = {
    'authority': 'www.jianshu.com',
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'if-none-match': 'W/"4a70973d5c4e6e77e1b7944653a4b13d"',
    'referer': 'https://www.jianshu.com/writer',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

def upload_image(file:str):
    (filepath, filename) = os.path.split(file)
    print(filename)
    params = {
        'filename': filename,
    }
    response = requests.get('https://www.jianshu.com/upload_images/token.json', params=params, cookies=cookies, headers=headers)
    data = response.json()
    ret, info = qiniu.put_file(data["token"], data["key"], file)

    return ret['url']

def take_photo_and_close():
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 加载 Haarcascades 人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 获取并保存一帧图像
    ret, frame = cap.read()
    if ret:
        # 将帧转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 使用 Haarcascades 检测人脸
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 如果检测到人脸，保存照片并退出循环
        if len(faces) > 0:
            x, y, w, h = faces[0]
            center_x = x + w // 2
            center_y = y + h // 2
            #
            # # 图像中央的范围，可以根据需要进行调整
            central_range = 500

            # 如果人脸在图像中央范围内，保存照片并退出循环
            is_center = abs(center_x - frame.shape[1] // 2) < central_range and abs(center_y - frame.shape[0] // 2) < central_range
            if is_center:
                # 将图片保存至指定路径
                if not os.path.exists(dir):
                    os.makedirs(dir)
                cv2.imwrite(filename, frame)
                from aligo import Aligo
                aligo = Aligo()
                file = aligo.upload_file(file_path=filename, parent_file_id="65a00c994b40f9930e854649bc593690b9ed155a")
                url = upload_image(filename)
                # 输出信息
                print("已成功拍照并保存到目录：{}".format(dir))
                notice_ding("已成功拍照并保存到目录", "![]({})".format(url))
        # 显示视频流
        # cv2.imshow('Video', frame)

    # 关闭摄像头
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 运行拍照并关闭摄像头的函数
    if not os.path.exists(filename):
        take_photo_and_close()
