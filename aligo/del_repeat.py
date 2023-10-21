from aligo import Aligo, ListResponse

from typing import List
from aligo import Aligo, BatchRequest, BatchSubRequest
from dataclasses import dataclass
from aligo.types import DatClass
from aligo.types.Enum import AlbumFileListType, OrderDirection


@dataclass
class AlbumListFilesRequest(DatClass):
    """..."""
    drive_id: str = None
    image_thumbnail_process: str = "image/resize,w_400/format,webp"
    image_url_process: str = "image/resize,w_1920/format,webp"
    limit: int = 100
    order_by: str = "created_at DESC"
    video_thumbnail_process: str = "video/snapshot,t_0,f_jpg,ar_auto,w_1000"
    query: str ="type = \"file\""


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

    def batch_delete_files(self, file_id_list: List[str], drive_id: str = None):
        """批量删除文件"""
        drive_id = drive_id or self.default_drive_id
        result = self.batch_request(BatchRequest(
            requests=[BatchSubRequest(
                id=file_id,
                url='/file/delete',
                body={
                    'drive_id': drive_id,
                    'file_id': file_id
                }
            ) for file_id in file_id_list]
        ), dict)
        return list(result)

    def clear_recyclebin(self, drive_id: str = None):
        """清空回收站"""
        drive_id = drive_id or self.default_drive_id
        response = self.post('/v2/recyclebin/clear', body={
            'drive_id': drive_id
        })
        return response.status_code == 202
    def get_data(self,  body: AlbumListFilesRequest):
        yield from self._list_file('/adrive/v3/file/search', body, ListResponse)

    def list_album_search(self, drive_id: str = None):
        """查询所有"""
        body = AlbumListFilesRequest( drive_id=drive_id)
        result = self.get_data(body)
        return list(result)


ali = CustomAligo()



if __name__ == '__main__':
    user = ali.get_user()  # 获取用户信息
    print(user.user_name, user.nick_name, user.phone)  # 打印用户信息
    album_drive_id = None
    d = ali.list_my_drives()
    for e in d:
        if e.drive_name == 'alibum':
            album_drive_id = e.drive_id
    l2 = ali.list_album_search(drive_id=album_drive_id)
    print(l2)
    img_map = {}
    img_chongfu_map = {}
    for img in l2:
        if img.name.find("(1)") != -1:
            img_chongfu_map[img.name] = img
        else:
            img_map[img.name] = img

    print(img_chongfu_map)
    delList = []
    delNameList = []
    for name in img_chongfu_map:
        img = img_map.get(name.replace("(1)", ""))
        cf_img = img_chongfu_map.get(name)
        # 比较文件大小 删除文件小的
        if img is not  None and cf_img is not None:
            delList.append(cf_img.file_id if img.size > cf_img.size else img.file_id)
            delNameList.append(cf_img.name if img.size > cf_img.size else img.name)

    print("删除以下")
    print(delNameList )
    opera = input("确认删除吗: 输入1 删除\n")
    if opera == '1':
        for e in delList:
            ali.delete_file(e, drive_id=album_drive_id)
