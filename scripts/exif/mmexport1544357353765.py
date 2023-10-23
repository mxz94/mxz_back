import os
from datetime import datetime

def timestamp_to_datetime_str(timestamp):
    # 将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(int(timestamp) / 1000)  # 将毫秒级时间戳转换为秒级时间戳
    # 将 datetime 对象格式化为字符串
    datetime_str = dt_object.strftime('%Y%m%d_%H%M%S')
    return datetime_str

# 调用函数进行转换

def filter_files_with_prefix(directory, prefix):
    files_with_prefix = []
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith("jpg"):
            times = filename.replace(prefix, "").split(".")[0]
            new_name = "IMG_"+ timestamp_to_datetime_str(times) + ".jpg"
            # 获取原文件的完整路径
            old_filepath = os.path.join(directory, filename)
            # 获取新文件的完整路径
            new_filepath = os.path.join(directory, new_name)
            # 重命名文件
            os.rename(old_filepath, new_filepath)
    return files_with_prefix

# 指定目录路径和文件名前缀
directory_path = r"G:\mxz\DCIM\2018-2020\WeiXin\马村"  # 替换为实际的目录路径
file_prefix = "mmexport"

filter_files_with_prefix(directory_path, file_prefix)

