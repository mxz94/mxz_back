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

def getCookies():
    import http.cookies
    with open(r"D:\mxz\mxz_back\scripts\writenote\cookies.txt", "r", encoding="utf8") as f:
        raw_cookie_string = f.read()
    cookies_dict = http.cookies.SimpleCookie()
    cookies_dict.load(raw_cookie_string)

    # 转换为 JSON 对象
    return  {key: morsel.value for key, morsel in cookies_dict.items()}

cookies = getCookies()

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
        # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

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
