import cv2

def take_photo_and_close():
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 获取并保存一帧图像
    ret, frame = cap.read()
    if ret:
        # 将图片保存至指定路径，这里假设是用户桌面
        cv2.imwrite(r'C:\Users\YourUsername\Desktop\auto_photo.jpg', frame)

    # 关闭摄像头
    cap.release()

    # 输出信息
    if ret:
        print("已成功拍摄照片并保存到桌面为 'auto_photo.jpg'")
    else:
        print("无法从摄像头获取图像")

# 运行拍照并关闭摄像头的函数
take_photo_and_close()