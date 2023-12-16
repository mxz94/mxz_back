import os

# 读取文件夹下所有文件
class FileUtils:
    @staticmethod
    def read_all_file(path):
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list


if __name__ == '__main__':
    print(FileUtils.read_all_file(r"D:\mxz\docker"))