import os

# 生成reademe

# 指定目录路径
directory_path = "./note_o"

# 使用os.listdir()获取目录下所有文件和文件夹的列表
file_names = os.listdir(directory_path)
s = {}
# 遍历文件名列表并打印
for file_name in file_names:
    if not os.path.isfile(os.path.join(directory_path, file_name)):
        s[file_name] = []
        file_names2 = os.listdir(os.path.join(directory_path, file_name))
        for file_name2 in file_names2:
            s[file_name].append("[{}]({})".format(file_name2.split(".")[0], directory_path + "/"+ file_name + "/" + file_name2))

re_s = reversed(s.items())
for key, value in re_s:
    value.reverse()

re_s = reversed(s.items())

dd = '''
<details {}><summary>{}</summary>
<p>

{}

</p>
</details>
'''
file_path = "../../content/README.md"  # 替换为你想要创建的文件路径
with open(file_path, 'w', encoding='utf-8') as file:
    open = "open"
    for key, value in re_s:
        content = ""
        for item in value:
            content += item + "<br>\n"
            # file.write(item + "<br>\n")
        file.write(dd.format(open,key, content))
        open = ""