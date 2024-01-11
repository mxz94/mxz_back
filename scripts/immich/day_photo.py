import datetime
import os
import subprocess

# 获取当前日期并以字符串的形式保存
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# 调用 Windows 11 相机应用程序并自动拍照
subprocess.call(['ms-photos://takephoto'])

# 在当前目录中创建以当天时间命名的图像文件夹
image_directory = os.path.join(os.getcwd(), current_date)
os.makedirs(image_directory, exist_ok=True)

# 将照片从相机应用程序保存到图像文件夹中
subprocess.call(['ms-photos://selectall', 'ms-photos://saveas', image_directory])

# 自动关闭相机应用程序
subprocess.call(['taskkill', '/f', '/im', 'Camera.exe'])

print(f"拍照成功，照片已保存至 {image_directory} 目录中。")