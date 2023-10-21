import psycopg2
from aligo import Aligo, BaseFile

conn = psycopg2.connect(database="immich", user="postgres", password="postgres", host="127.0.0.1", port="54321")


cur = conn.cursor()
cur.execute('''

SELECT * from ali_albums where 
split_part(name, '.', 1) NOT in (SELECT  "originalFileName"
from  assets)    ORDER BY time desc, created_at asc 

''')
ht = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" name="referrer" content="no-referrer"/>
    <title>Title</title>
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
</head>
<body>
<div id="app">
    <table>

'''

rows = cur.fetchall()
ali = Aligo()  # 第一次使用，会弹出二维码，供扫描登录
print(ali.list_albums(drive_id="9771618"))
# 9yxi9ZuqqAJ
s = []
for row in rows:
    a = '''
           <tr style="width:300px">
            <td style=" width: 160px">  <img src="{}" style="height: 160px; width: 160px" name="{}"></td>
            <td style=" width: 160px fl"> <el-button @mouseover.native="hah('{}')">{}</el-button></td>
             <td style=" width: 160px fl"> {}</td>
        </tr>
    '''.format(row[5], row[2], row[1], row[2], row[6])
    ht = ht + a
    s.append(BaseFile(file_id=row[1], drive_id="9771618"))
    ali.download_file(file_id=row[1], drive_id="9771618", local_folder= "/temp")
    if (len(s) == 20):
        ali.add_files_to_album(album_id='9yxi9ZuqqAJ', files=s)
        s = []
ht = ht + '''
    </table>
</div>
</body>

<script src="https://unpkg.com/vue@2/dist/vue.js"></script>
<!-- import JavaScript -->
<script src="https://unpkg.com/element-ui/lib/index.js"></script>
<script>
    new Vue({
        el: '#app',
        data: function() {
            return { visible: false }
        },
        methods: {
            hah(fileId) {
                const url = 'http://127.0.0.1:8080/hello/'+fileId
                fetch(url).then(data => console.log(data))
            }
        }
    })
</script>
</html>
'''
with open("test232.html", "w") as file:
    file.write(ht)