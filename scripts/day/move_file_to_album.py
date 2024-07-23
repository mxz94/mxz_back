from aligo import Aligo

from scripts.utils.aligo_utils import CustomAligo

aligo = CustomAligo()
# aligo.add_files_to_album()
# drive = aligo.get_default_drive()
# print(drive)
#  我的
file_id  = '657c27afd54cd6a0ad8546d2902c69867591a8c3'
f_list = aligo.get_file_list(drive_id=str(79808), parent_file_id=file_id)
for f in f_list:
    print(f)
file_id = '668f3fa72d62252101cb408fbc138e035fba6ff2'
# albums = aligo.list_albums()
# for album in albums:
#     print(album)
# 电脑
album_id = 'kiHasaNX8G3'

file_list = aligo.get_file_list(parent_file_id=file_id, drive_id=str(79808))
aligo.add_files_to_album(album_id, file_list)