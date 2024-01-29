import json
import os
from typing import Callable

from aligo import Aligo, BaseFile, GetFileRequest, GetFileListRequest
class CustomAligo(Aligo):
    """自定义 aligo """
    V3_FILE_DELETE = '/v3/file/delete'
    def delete_file(self, file_id: str, drive_id: str = None) -> bool:
        """删除文件"""
        drive_id = drive_id or self.default_drive_id
        response = self.post(self.V3_FILE_DELETE, body={
            'drive_id': drive_id,
            'file_id': file_id
        })
        return response.status_code == 204

    def download_folder(self, folder_file_id: str, local_folder: str = '.', drive_id: str = None,
                        file_filter: Callable[[BaseFile], bool] = lambda x: False) -> str:
        """
        下载文件夹
        :param folder_file_id: [str] 文件夹 id
        :param local_folder: [str] 本地文件夹路径, 默认为当前目录, 即下载到哪里
        :param drive_id: [str] 文件夹所在的网盘 id
        :param file_filter: 文件过滤函数
        :return: [str] 本地文件夹路径

        用法示例:
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> result = ali.download_folder(folder_file_id='<folder_file_id>')
        >>> print(result)
        """
        if folder_file_id != 'root':
            folder = self._core_get_file(GetFileRequest(file_id=folder_file_id, drive_id=drive_id))
            local_folder = os.path.join(local_folder, self._del_special_symbol(folder.name))
        return self.__download_folder(folder_file_id, local_folder, drive_id, file_filter=file_filter)

    def __download_folder(self, folder_file_id: str, local_folder: str = '.', drive_id: str = None,
                          file_filter: Callable[[BaseFile], bool] = lambda x: False) -> str:
        """下载文件夹"""
        # 创建文件夹, 即使文件夹为空
        os.makedirs(local_folder, exist_ok=True)
        files = []
        for file in self._core_get_file_list(GetFileListRequest(parent_file_id=folder_file_id, drive_id=drive_id)):
            if file_filter(file):
                continue
            if file.type == 'folder':
                self.__download_folder(folder_file_id=file.file_id,
                                       local_folder=os.path.join(local_folder, self._del_special_symbol(file.name)), drive_id=drive_id)
                continue
            print(file)
            files.append(file)
        self.download_files(files, local_folder=local_folder)
        return os.path.abspath(local_folder)
ali = CustomAligo()  # 第一次使用，会弹出二维码，供扫描登录
# 资源库
drive_id = str(645810972)
# 备份库
d2_id = str(79808)

file_id = "65b0acfdc028637ce82b4c0d8655329e0965893a"
print(ali.get_file_list(drive_id=drive_id, parent_file_id=file_id))
# print(ali.get_file_list(parent_file_id="65b0adf486280f1aaf074b2e96ae55846f6e8ca8"))
# local = "/ql/data/mxz_back/"
# ali.download_folder(folder_file_id=file_id, local_folder=local, drive_id=drive_id)