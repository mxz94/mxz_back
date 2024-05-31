import os

src = "D:/mxz/mxz_back"

def move_first_to_last(my_list):
    if len(my_list) >= 2:
        first_element = my_list.pop(0)
        my_list.append(first_element)

class Article:
    def __init__(self, var1, var2, var3, var4):
        self.pubDatetime = var1
        self.title = var2
        self.slug = var3
        self.tags = var4

def get_article_attrs(file_path:str):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hasTag = False
        tags = []
        for line in lines:
            if "pubDatetime" in line:
                pubDatetime = line.split(": ", 1)[1]
            if "title" in line:
                title = line.split(": ", 1)[1]
            if "slug" in line:
                slug = line.split(": ", 1)[1]
            if hasTag and "- " in line:
                tagstr = line.split('"')
                tags.append(tagstr[1])
            if "tags" in line: hasTag = True
        return Article(pubDatetime, title, slug, tags)

def init_archives_table_readme():
    url = "https://malanxi.top/blog/"
    # 指定目录路径
    directory_path = src + "/src/content/blog"
    article_url = '<li class="mt-3 mb-3"><a href="{}">{}</a></li>'
    # 使用os.listdir()获取目录下所有文件和文件夹的列表
    file_names = os.listdir(directory_path)
    s = {}
    for dir_name in file_names:
        list = []
        if dir_name.startswith("20"):
            m_d = {}
            s[dir_name] = m_d
            file_list = os.listdir(os.path.join(directory_path, dir_name))
            list += reversed(file_list)
            if "展望" in list[0]:
                    move_first_to_last(list)
            for file_name2 in list:
                title = file_name2.split(".")[0]
                u = title.replace(" ","")
                month = title[0:7]
                if m_d.get(month) is None:
                    m_d[month] = []
                m_d[month].append(article_url.format(url + u, title, ))
        else:
            m_d = {}
            s[dir_name] = m_d
            file_list = os.listdir(os.path.join(directory_path, dir_name))
            # file_list = sorted(file_list, key=lambda x: os.path.getctime(os.path.join(os.path.join(directory_path, dir_name), x)), reverse=True)
            file_list = sorted(file_list, key=lambda x: get_article_attrs(os.path.join(os.path.join(directory_path, dir_name), x)).pubDatetime, reverse=True)
            for file in file_list:
                title = file.split(".")[0]
                month = get_article_attrs(os.path.join(os.path.join(directory_path, dir_name), file)).pubDatetime[0:7]
                if m_d.get(month) is None:
                    m_d[month] = []
                m_d[month].append(article_url.format(url + title, title, ))
#                 s[dir_name].append(article_url.format(url + u, title, ))
    re_s = reversed(s.items())
    for key, value in re_s:
        start = '''---
    import BaseLayout from "../../../layouts/BaseLayout.astro";
    import TimeLineElement from "../../../components/cv/TimeLine.astro";
    ---
    
    <BaseLayout title="Resume" sideBarActiveItemID="cv">
      <div class="mb-5">
        <div class="text-3xl w-full font-bold">Blog</div>
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
        file_path = src + "/src/pages/blog/archives"
        tlist = []
        with open(file_path+"/"+ str(key)+".astro", 'w', encoding='utf-8') as file:
            for month, article in value.items():
                tlist.append(TimeLineElement.format(month, "\n".join(article)))
            file.write(start.format("\n".join(tlist)))
if __name__ == '__main__':
    init_archives_table_readme()