import datetime
import os

import cv2
import qiniu
import requests

now = datetime.datetime.now()
year = now.strftime("%Y")
name = now.strftime("%Y-%m-%d")


def notice_ding(title, content):
    json_data = {"title":title,"content":content,}
    response = requests.post('https://xizhi.qqoq.net/XZb02fde849963687f64a219eafba83a6b.send', json=json_data)
    print(response.json())

dir = r'D:\Program Files\Pictures\profile\{}'.format(year)
filename = dir+ r'\{}.jpg'.format(name)

def upload_image(file:str):
    (filepath, filename) = os.path.split(file)
    headers = {
        "Authorization" : "Bearer "+"149|TByGbpkb7ePEiIhEzyIm1f0hf6E3WRF2YkRChide",
        "Content-Type" : "multipart/form-data",
        "Accept" : "application/json"
    }
    files = {'file': (filename, open(file, 'rb'), 'application/json')}
    res = requests.post("https://www.freeimg.cn/api/v1/upload", files=files, headers=headers)
    return res.json()["data"]["links"]["url"]

def take_photo_and_close():
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
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
                if os.path.exists(filename):
                    try:
                        os.remove(filename)
                    except Exception as e:
                        print(f"删除文件时发生错误: {e}")           # 将图片保存至指定路径
                if not os.path.exists(dir):
                    os.makedirs(dir)
                cv2.imwrite(filename, frame)
                url = upload_image(filename)
                # 输出信息
                notice_ding("已成功拍照并保存到目录", "![]({})".format(url))
        # 显示视频流
        # cv2.imshow('Video', frame)

    # 关闭摄像头
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 运行拍照并关闭摄像头的函数
    take_photo_and_close()
