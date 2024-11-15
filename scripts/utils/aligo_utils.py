from dataclasses import dataclass

from aligo import ListResponse, MoveFileRequest, BatchMoveFilesRequest, BatchSubResponse, \
    MoveFileResponse

from typing import List, Iterator

from aligo import Aligo, BatchRequest, BatchSubRequest
from aligo import ListResponse, MoveFileRequest, BatchMoveFilesRequest, BatchSubResponse, \
    MoveFileResponse
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
    V3_BATCH = '/v3/batch'


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

    def share_album_list(self):
        response = self.post(self.V1_COPY_SHARE_LIST, body={}, host="https://api.alipan.com/adrive")
        return response

    def batch_move_(self, file_id_list: List[str], drive_id: str = None):
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

    def _core_batch_move_files(self, body: BatchMoveFilesRequest) -> Iterator[BatchSubResponse[MoveFileResponse]]:
        """..."""
        if body.drive_id is None:
            body.drive_id = self.default_drive_id

        yield from self.batch_request(BatchRequest(
            requests=[BatchSubRequest(
                id=file_id,
                url='/file/move',
                body=MoveFileRequest(
                    drive_id=body.drive_id, file_id=file_id,
                    to_parent_file_id=body.to_parent_file_id,
                    overwrite=body.overwrite, auto_rename=body.auto_rename, to_drive_id='9771618'
                )
            ) for file_id in body.file_id_list]
        ), MoveFileResponse)

    def batch_move_files_2(self,
                           file_id_list: List[str] = None,
                           to_parent_file_id: str = 'root',
                           drive_id: str = None,
                           to_drive_id: str = None,
                           body: BatchMoveFilesRequest = None,
                           **kwargs) -> List[BatchSubResponse[MoveFileResponse]]:
        if body is None:
            body = BatchMoveFilesRequest(
                drive_id=drive_id,
                file_id_list=file_id_list,
                to_parent_file_id=to_parent_file_id,
                **kwargs
            )
        if body.drive_id is None:
            body.drive_id = self.default_drive_id
        result = self._core_batch_move_files2(body, to_drive_id)
        return list(result)




ali = CustomAligo()

if __name__ == '__main__':
    file_id = "67219ca387f42ee4d9bb4275af78d68bacefe10b"
    file = "./dd.7z"
    ali.uplo(file, file_id)