import datetime
import os

import cv2
import qiniu
import requests
from qiniu import Auth, put_file

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
def upload_image_file(file):
    try:
        access_key = "Y07Awc_13lhWdx-VS3Z78uCYxvgHDf19FJ4ousBc"
        secret_key = "3mD6dDLqur1M9yKoZG53qov-JS-7WVkOBD0SoeGj"
        url = "http://s9yka7j04.sabkt.gdipper.com/"
        q = Auth(access_key, secret_key)
        bucket_name = 'mxz9'
        #上传后保存的文件名
        path, name = os.path.split(file)
        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, name, 3600)
        #要上传文件的本地路径
        ret, info = put_file(token, name, file, version='v2')
        return url + name
    except Exception as e:
        print(" # 上传失败")
        return None

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
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

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
                url = upload_image_file(filename)
                # 输出信息
                print("已成功拍照并保存到目录：{}".format(dir))
                notice_ding("已成功拍照并保存到目录", "![]({})".format(url))
        # 显示视频流
        # cv2.imshow('Video', frame)

    # 关闭摄像头
    cap.release()
    cv2.destroyAllWindows()

os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'

if __name__ == '__main__':
    # 运行拍照并关闭摄像头的函数
    if not os.path.exists(filename):
        take_photo_and_close()
