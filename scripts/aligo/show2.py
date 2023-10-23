import os

import psycopg2
from aligo import Aligo, BaseFile
import shutil

conn = psycopg2.connect(database="immich", user="postgres", password="postgres", host="127.0.0.1", port="54321")


cur = conn.cursor()
cur.execute('''
SELECT name, "substring"(time, 0, 5) from ali_albums where 
split_part(name, '.', 1) NOT in (SELECT  "originalFileName"
from  assets)    and  name not like '%livp%' and time is null ORDER BY time desc, created_at asc 

''')

source_file_path = "D:/new/"
destination_folder = "D:/new2/"

rows = cur.fetchall()
for row in rows:
    print(row)
    # os.makedirs(destination_folder + row[1] + "/", exist_ok=True)
    # try:
    #     shutil.copy(source_file_path + row[0], destination_folder + row[1] + "/")
    # except Exception as e:
    #     print(e)