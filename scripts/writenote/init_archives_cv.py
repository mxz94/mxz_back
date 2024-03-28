import os

src = "D:/mxz/mxz_back"

def move_first_to_last(my_list):
    if len(my_list) >= 2:
        first_element = my_list.pop(0)
        my_list.append(first_element)

def init_archives_table_readme():
    url = "https://mxz94.asia/blog/"
    # 指定目录路径
    directory_path = src + "/src/content/blog"
    article_url = '<li class="mt-3 mb-3"><a href="{}">{}</a></li>'
    # 使用os.listdir()获取目录下所有文件和文件夹的列表
    file_names = os.listdir(directory_path)
    s = {}
    # 遍历文件名列表并打印

    for dir_name in file_names:
        list = []
        if not os.path.isfile(os.path.join(directory_path, dir_name)):
            m_d = {}
            s[dir_name] = m_d
            file_list = os.listdir(os.path.join(directory_path, dir_name))
            list += reversed(file_list)
            if "展望" in list[0]:
                    move_first_to_last(list)
            for file_name2 in list:
                title = file_name2.split(".")[0]
                u = title.replace(" ","")
                if (title.startswith("20")):
                    month = title[0:7]
                else:
                    month = "2024-10"
                if m_d.get(month) is None:
                    m_d[month] = []
                m_d[month].append(article_url.format(url + u, title, ))
#                 s[dir_name].append(article_url.format(url + u, title, ))
    re_s = reversed(s.items())
    for key, value in re_s:
        start = '''---
    import BaseLayout from "../../../layouts/BaseLayout.astro";
    import TimeLineElement from "../../../components/cv/TimeLine.astro";
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
               {}
    
        </TimeLineElement>'''
        file_path = src + "/src/pages/note/archives"
        tlist = []
        with open(file_path+"/"+ str(key)+".astro", 'w', encoding='utf-8') as file:
            for month, article in value.items():
                tlist.append(TimeLineElement.format(month, "\n".join(article)))
            file.write(start.format("\n".join(tlist)))
if __name__ == '__main__':
    init_archives_table_readme()