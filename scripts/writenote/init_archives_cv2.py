import os

src = "D:/mxz/mxz_back"

def move_first_to_last(my_list):
    if len(my_list) >= 2:
        first_element = my_list.pop(0)
        my_list.append(first_element)

def init_archives_table_readme():
    url = "https://mxz94.asia/blog/"
    url_note = "https://mxz94.asia/note/"
    # 指定目录路径
    directory_path_list = [src + "/src/content/blog", src + "/src/content/note"]
    list = []
    article_url = '<li><a href="{}">{}</a></li>'
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
                        s[file_name].append(article_url.format(url + u, title, ))
                    else:
                        s[file_name].append(article_url.format(url_note + u, title))
            else:
                if (not s.keys().__contains__("note")):
                    s["note"] = []
                title = file_name.split(".")[0]
                u = title.replace(" ","")
                s["note"].append(article_url.format(url_note + u, title))
        re_s = reversed(s.items())
        for key, value in re_s:
            value.reverse()
            if key.startswith("20") and value[0].endswith("展望)"):
                move_first_to_last(value)

        list += reversed(s.items())

    start = '''---
import BaseLayout from "../layouts/BaseLayout.astro";
import TimeLineElement from "../components/cv/TimeLine.astro";
---

<BaseLayout title="Resume" sideBarActiveItemID="cv">
  <div class="mb-5">
    <div class="text-3xl w-full font-bold">Note</div>
  </div>

  <div class="time-line-container mb-10">
    {}
  </div>
</BaseLayout>
'''
    TimeLineElement = '''<TimeLineElement
      title="{}"
    >
    <ul class="list-disc md:columns-3 columns-33 mx-9">
           {}
    </ul>

    </TimeLineElement>'''
    file_path = src + "/src/pages/lifemap.astro"  # 替换为你想要创建的文件路径
    with open(file_path, 'w', encoding='utf-8') as file:
        tlist = []
        for key, value in list:
            tlist.append(TimeLineElement.format(key, "".join(value)))

        start = start.format("".join(tlist))
        file.write(start)
if __name__ == '__main__':
    init_archives_table_readme()