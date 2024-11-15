import os
import pyminizip

def compress_and_encrypt(folder_path, output_zip, password):
    # 获取文件夹中的所有文件
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    # 压缩并加密
    pyminizip.compress_multiple(files, [], output_zip, password, 5)

# 使用示例
folder_to_compress = r'D:\mxz\mxz_back\public'
output_zip_file = r'D:\mxz\tmp\1'
encryption_password = 'yourpassword'

compress_and_encrypt(folder_to_compress, output_zip_file, encryption_password)