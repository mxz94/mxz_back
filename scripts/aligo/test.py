import os
import sqlite3
import time
from typing import List

import aligo
from aligo import BaseFile

from scripts.aligo import aligo_utils
from 简书.writejianshu.jian_utils import FileUtil

con = sqlite3.connect("ali.db")
ali = aligo_utils.ali


def hahha(path, a):
    try:
        device_name = None
        if a.user_tags:
            device_name = a.user_tags.get("device_name")
        sql = f'replace INTO "ali_albums_mxz_all" ("channel", "drive_id", "size", "name", "device_name", "file_id", "path") VALUES ("{a.channel}", "{a.drive_id}", {a.size}, "{a.name}", "{device_name}", "{a.file_id}", "{path}");'
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
    except Exception as e:
        print(e)

def file_to_db(parent_file_id: str, drive_id: str):
    ali.walk_files(callback=hahha, parent_file_id=parent_file_id, drive_id=drive_id)

def file_to_album():
    year = ""
    cur = con.cursor()
    cur.execute(f"SELECT drive_id, file_id from ali_albums_mxz_all where path like '{year}%'")
    list = cur.fetchall()
    a = []
    for e in list:
        a.append(e[1])
    b = [a[i:i+300] for i in range(0,len(a),300)]
    print(list.__len__())
    # file_id_list: List[str] = None,
    #
    for e in b:
        print(ali.batch_move_files(file_id_list=e, drive_id=drive_id, to_drive_id=to_drive_id))


def in_db(fileList: List[BaseFile]):
    try:
        for a in fileList:
            device_name = None
            if a.user_tags:
                device_name = a.user_tags.get("device_name")
            sql = f'replace INTO "ali_albums" ("channel", "drive_id", "size", "name", "device_name", "file_id") VALUES ("{a.channel}", "{a.drive_id}", {a.size}, "{a.name}", "{device_name}", "{a.file_id}");'
            # print(sql)
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
    except Exception as e:
        print(e)
down_album_id = "DFnEEDFoNXe"
def down():
    cur = con.cursor()
    cur.execute("SELECT file_id, path from ali_albums_all where name in (SELECT name FROM ali_albums) and size <8118983921  ORDER BY size")
    list = cur.fetchall()
    for i in list:
        fle_id = i[0]
        path = i[1]
        local_folder = os.path.join(r"D:\tmp\p", path)
        FileUtil.check_dir(local_folder)
        print(local_folder)
        ali.download_file(file_id= fle_id, drive_id="440134182", local_folder=local_folder)
def delete_file():
    con = sqlite3.connect("ali.db")
    cur = con.cursor()
    cur.execute("SELECT drive_id, file_id FROM ali_albums_mxz where  device_name != 'iPhone14,8'")
    data = cur.fetchall()
    a = []
    for datum in data:
        a.append(datum[1])
        if a.__len__() == 50:
            ali.batch_delete_files(a, drive_id= datum[0])
            a = []
            time.sleep(1)
# down()
for list_my_drive in ali.list_my_drives():
    print(list_my_drive.drive_name, list_my_drive.drive_id)

# for get_file in (ali.get_file_list(drive_id="96852261")):
#     print(get_file.to_dict())
    # asd()
    # p = "6545f7f0416e83f453a6472b92241dfd123c7367"
    # file_to_db(p)
# for get_file in ali.get_file_list(parent_file_id="654503f04e889bacad0e435aa3cbddd0264d0d2c"):
#     print(get_file)

# drive_id = "96852261"

# drive_id = '96852261'
# to_drive_id = '23912261'
# ali.batch_move_files()
drive_id = '79808'
to_drive_id = '9771618'
# for get_file in ali.get_file_list(drive_id=drive_id):
#     print(get_file)
# file_to_db("65459d5a391c6c693dec447794ba58faac3aae5b", drive_id)
file_to_album()
# file_to_album()

# size = 0
# for list_album in ali.list_albums(drive_id=drive_id):
#     if list_album.total_count is not  None:
#         year = list_album.name
#         cur = con.cursor()
#         cur.execute(f"SELECT drive_id, file_id from ali_albums2 where path like '{year}%'")
#         list = cur.fetchall()
#         size = size + list.__len__()
#         print(year, list_album.total_count)
# print(size)

# delete_file()

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
# for a in ali.list_album_search("9771618"):
#     try:
#         device_name = None
#         if a.user_tags:
#             device_name = a.user_tags.get("device_name")
#         sql = f'replace INTO "ali_albums_mxz" ("channel", "drive_id", "size", "name", "device_name", "file_id") VALUES ("{a.channel}", "{a.drive_id}", {a.size}, "{a.name}", "{device_name}", "{a.file_id}");'
#         # print(sql)
#         cur = con.cursor()
#         cur.execute(sql)
#         con.commit()
#     except Exception as e:
#         print(e)