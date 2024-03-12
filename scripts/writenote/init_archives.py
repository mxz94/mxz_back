import os

src = "D:/mxz/mxz_back"

def move_first_to_last(my_list):
    if len(my_list) >= 2:
        first_element = my_list.pop(0)
        my_list.append(first_element)

def init_archives_table_readme():
    url = "https://mxz-back.pages.dev/blog/"
    url_note = "https://mxz-back.pages.dev/note/"
    # 指定目录路径
    directory_path_list = [src + "/src/content/blog", src + "/src/content/note"]
    list = []
    for directory_path in directory_path_list:

        # 使用os.listdir()获取目录下所有文件和文件夹的列表
        file_names = os.listdir(directory_path)
        s = {}
        # 遍历文件名列表并打印

        for file_name in file_names:
            if not os.path.isfile(os.path.join(directory_path, file_name)):
                s[file_name] = []
                file_names2 = []
                for  root, dirs, files in os.walk(os.path.join(directory_path, file_name)):
                    file_names2 += files
                for file_name2 in file_names2:
                    title = file_name2.split(".")[0]
                    u = title.replace(" ","")
                    if u.startswith("20"):
                        s[file_name].append("[{}]({})".format(title, url + u))
                    else:
                        s[file_name].append("[{}]({})".format(title, url_note + u))
            else:
                if (not s.keys().__contains__("note")):
                    s["note"] = []
                title = file_name.split(".")[0]
                u = title.replace(" ","")
                s["note"].append("[{}]({})".format(title, url_note + u))
        re_s = reversed(s.items())
        for key, value in re_s:
            value.reverse()
            if key.startswith("20") and value[0].endswith("展望)"):
                move_first_to_last(value)

        list += reversed(s.items())

    start = '''---
layout: ../layouts/ArchivesLayout.astro
title: ""
---
<style>
td, th {
   border: none!important;
   font-size: .775em;
}
</style>
'''
    dd = '''

# [{}](https://mxz-back.pages.dev/blog/tag/{})

|        |         |        |
| ------------ |---------|---------|       
{}
        
        '''
    dd3 = '''|{}|{}|{}|
'''
    file_path = src + "/src/pages/archives.md"  # 替换为你想要创建的文件路径
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(start)
        for key, value in list:
            content = ""
            yu = value.__len__()%3
            index = (value.__len__())//3
            if (yu != 0):
                index = index + 1
            print(index)
            for i in range(0, index):
                v1 = value[i]
                if (i+index < value.__len__()):
                    v2 = value[i+index]
                else:
                    v2 = ""
                if (i+index*2 < value.__len__()):
                    v3 = value[i+index*2]
                else:
                    v3 = ""
                content += (dd3.format(v1, v2,v3))
            file.write(dd.format(key, key, content))

if __name__ == '__main__':
    init_archives_table_readme()