import json
import sqlite3
import time

from aligo import Aligo, ListResponse, BaseFile

from typing import List
from aligo import Aligo, BatchRequest, BatchSubRequest
from dataclasses import dataclass
from aligo.types import DatClass

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
    V1_COPY_SHARE = '/v1/sharedAlbum/copyFilesToAlbum'
    V1_COPY_SHARE_LIST = '/v1/sharedAlbum/list'

    def delete_file(self, file_id: str, drive_id: str = None) -> bool:
        """删除文件"""
        drive_id = drive_id or self.default_drive_id
        response = self.post(self.V3_FILE_DELETE, body={
            'drive_id': drive_id,
            'file_id': file_id
        })
        return response.status_code == 204

    def share_copy_files_to_album(self, fileId_list: List, drive_id, sharedAlbumId, toAlbumId):
        driveFileList = []
        for fileId in fileId_list:
            driveFileList.append({"drive_id", drive_id, "file_id", fileId})
        data = {
            "driveFileList": driveFileList,
            "sharedAlbumId": sharedAlbumId,
            "toAlbumId": toAlbumId
        }
        response = self.post(self.V1_COPY_SHARE, body=data, host="https://api.alipan.com/adrive")
        return response
    def share_album_list(self):
        response = self.post(self.V1_COPY_SHARE_LIST, body={}, host="https://api.alipan.com/adrive")
        return response
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
# for list_my_drive in ali.list_my_drives():
#     print(list_my_drive.category, list_my_drive.drive_id)
# for get_file in (ali.get_file_list(drive_id="96852261")):
#     print(get_file.to_dict())
parent_file_id = "654501a3cc1dedb5eb12438f8a1687ee3b0ab8e3"
drive_id = "96852261"

con = sqlite3.connect("ali.db")

# def hahha(path, a):
#     try:
#         device_name = None
#         if a.user_tags:
#             device_name = a.user_tags.get("device_name")
#         sql = f'replace INTO "ali_albums2" ("channel", "drive_id", "size", "name", "device_name", "file_id", "path") VALUES ("{a.channel}", "{a.drive_id}", {a.size}, "{a.name}", "{device_name}", "{a.file_id}", "{path}");'
#         # print(sql)
#         cur = con.cursor()
#         cur.execute(sql)
#         con.commit()
#     except Exception as e:
#         print(e)
#
# ali.walk_files(callback=hahha, parent_file_id=parent_file_id)

for list_album in ali.list_albums(drive_id=drive_id):
    print(list_album.to_dict())

# album_id = "FByMnXDC65h"
# year = "电脑"
# cur = con.cursor()
# cur.execute(f"SELECT drive_id, file_id from ali_albums2 where path like '{year}%'")
# list = cur.fetchall()
# a = []
# for e in list:
#     a.append(BaseFile(drive_id=e[0], file_id= e[1]))
# b = [a[i:i+300] for i in range(0,len(a),300)]
# for e in b:
#     ali.add_files_to_album(album_id=album_id, files=e)
# print(ali.get_album(album_id).file_count)
# print(list.__len__() == ali.get_album(album_id).file_count)
# print(a)
# for get_file in ali.get_file_list(parent_file_id="654501a3cc1dedb5eb12438f8a1687ee3b0ab8e3"):
#     ali.create_album(get_file.name)



al = ali.list_album_files(album_id="pXwJyoDpb7y")
for e in al:
    con = sqlite3.connect("ali.db")
    cur = con.cursor()
    cur.execute(f"SELECT drive_id, file_id FROM ali_albums where name = '{e.name}'")
    data = cur.fetchall()
    print(e.name)
# con = sqlite3.connect("ali.db")
# cur = con.cursor()
# cur.execute("SELECT drive_id, file_id FROM ali_albums where drive_id = '23912261'  and device_name != 'iPhone14,8'")
# data = cur.fetchall()
# a = []
# for datum in data:
#     a.append(datum[1])
#     if a.__len__() == 50:
#         ali.batch_delete_files(a, drive_id= datum[0])
#         a = []
#         time.sleep(1)
#
# # ali.delete_file("6544b8c3bf6570e4ef314afcb5b9418df1b8c4f0", drive_id="23912261")
# ali.clear_recyclebin(drive_id="23912261")
# print(ali.list_albums())
# ali.add_files_to_album("3NDjHreTLZf", [BaseFile(drive_id="440134182", file_id="65139c02c557bf1b961c4567a07c9025a542b038")])
# drive_id = next((drive.drive_id for drive in ali.list_my_drives() if drive.drive_name == 'alibum'), None)

# data = None
# with open("a.json", "r", encoding="utf-8") as f:
#     data = json.loads(f.read())
#
# print(data)

#
# for a in ali.list_album_search(drive_id):
#     try:
#         device_name = None
#         if a.user_tags:
#             device_name = a.user_tags.get("device_name")
#         sql = f'replace INTO "ali_albums" ("channel", "drive_id", "size", "name", "device_name", "file_id") VALUES ("{a.channel}", "{a.drive_id}", {a.size}, "{a.name}", "{device_name}", "{a.file_id}");'
#         # print(sql)
#         cur = con.cursor()
#         cur.execute(sql)
#         con.commit()
#     except Exception as e:
#         print(e)