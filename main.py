# -*- coding: utf-8 -*-
import argparse
import json
import os
import random
import re
from datetime import timedelta, datetime

import requests
from github import Github

NOTE_DIR = "src/content/note"
NOTE_IMG = "public/img/note"

TABLE_DIR = {
    "note": {
        "img": "public/img/note",
        "dir": "src/content/note",
        "ref_dir": "(../../../public/img/note/{})"
    },
    "朝花夕拾": {
        "img": "public/img/zhxs",
        "dir": "src/content/blog/朝花夕拾",
        "ref_dir": "(../../../../public/img/zhxs/{})"
    },
    "成长日记": {
        "img": "public/img/czrj",
        "dir": "src/content/blog/成长日记",
        "ref_dir": "(../../../../public/img/czrj/{})"
    },
    "2024": {
        "img": "public/img/2024",
        "dir": "src/content/blog/2024",
        "ref_dir": "(../../../../public/img/2024/{})"
    },
    "2025": {
        "img": "public/img/2025",
        "dir": "src/content/blog/2025",
        "ref_dir": "(../../../../public/img/2025/{})"
    },
    "2026": {
        "img": "public/img/2026",
        "dir": "src/content/blog/2026",
        "ref_dir": "(../../../../public/img/2026/{})"
    },
    "2027": {
        "img": "public/img/2027",
        "dir": "src/content/blog/2027",
        "ref_dir": "(../../../../public/img/2027/{})"
    }
}
DIR = TABLE_DIR["note"]

IMG_SAVE_LOCAL = True

class Article:
    def __init__(self, var1, var2, var3, var4):
        self.pubDatetime = var1
        self.title = var2
        self.slug = var3
        self.tags = var4
def move_first_to_last(my_list):
    if len(my_list) >= 2:
        first_element = my_list.pop(0)
        my_list.append(first_element)
def get_article_attrs(file_path:str):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        hasTag = False
        tags = []
        slug = None
        title = None
        for line in lines:
            line = line.replace("\n", "")
            if "pubDatetime" in line:
                pubDatetime = line.split(": ", 1)[1]
            if "title" in line:
                title = line.split(": ", 1)[1]
            if "slug" in line:
                slug = line.split(": ", 1)[1]
            if hasTag and "- " in line:
                tagstr = line.split('"')
                if tagstr.__len__() >= 2:
                    tagstr = line.split("- ")
                tags.append(tagstr[1])
            if "tags" in line: hasTag = True
            if title and "---" in line:
                break
        return Article(pubDatetime, title, slug, tags)
    except Exception as e:
        print(file_path)
def init_archives_table_readme():
    url = "https://malanxi.top/blog/"
    # 指定目录路径
    directory_path = "./src/content/blog"
    article_url = '<li class="mt-3 mb-3"><a href="{}">{}</a></li>'
    # 使用os.listdir()获取目录下所有文件和文件夹的列表
    file_names = os.listdir(directory_path)
    s = {}
    for dir_name in file_names:
        if dir_name.startswith("20"):
            m_d = {}
            s[dir_name] = m_d
            file_list = os.listdir(os.path.join(directory_path, dir_name))
            file_list = sorted(file_list, key=lambda x: get_article_attrs(os.path.join(os.path.join(directory_path, dir_name), x)).pubDatetime, reverse=True)
            for file_name2 in file_list:
                title = file_name2.split(".")[0]
                article = get_article_attrs(os.path.join(os.path.join(directory_path, dir_name), file_name2))
                if article.slug != None:
                    title = article.slug
                u = title.replace(" ","")
                month = title[0:7]
                if (not title.startswith(dir_name + "-")):
                    month = dir_name
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
                article = get_article_attrs(os.path.join(os.path.join(directory_path, dir_name), file))
                if article.slug != None:
                    title = article.slug
                month = article.pubDatetime[0:7]
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
        
        <BaseLayout title="{}">
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
        file_path = "./src/pages/blog/archives"
        tlist = []
        with open(file_path+"/"+ str(key)+".astro", 'w', encoding='utf-8') as file:
            for month, article in value.items():
                tlist.append(TimeLineElement.format(month, "\n".join(article)))
            file.write(start.format(str(key), "\n".join(tlist)))

def get_json_data():
    with open("src/issue.json", "r") as file:
        json_data = json.load(file)
    return json_data

def add_issue_id(id):
    with open("src/issue.json", "r") as file:
        json_data = json.load(file)
    if id not in json_data:
        json_data.append(id)
    with open("src/issue.json", "w") as file:
        json.dump(json_data, file)

def get_to_generate_issues(repo, issue_number=None):
    generated_issues_numbers = get_json_data()
    to_generate_issues = [
        i
        for i in list(repo.get_issues())
        if int(i.number) not in generated_issues_numbers
    ]
    if issue_number:
        to_generate_issues.append(repo.get_issue(int(issue_number)))
    return to_generate_issues

def check_dir(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)
def main(token, repo_name, issue_number=None):
    user = Github(token)
    me = user.get_user().login
    repo = user.get_repo(repo_name)
    to_generate_issues = get_to_generate_issues(repo, issue_number)
    for issue in to_generate_issues:
        labels = issue.labels
        no_finish = len(labels) > 0 and "no_finish" in [label.name for label in labels]
        if no_finish:
            continue
        global DIR
        DIR = TABLE_DIR["note"]
        if len(labels) > 0 and "朝花夕拾" in [label.name for label in labels]:
            DIR = TABLE_DIR.get("朝花夕拾")
        if len(labels) > 0 and "成长日记" in [label.name for label in labels]:
            DIR = TABLE_DIR.get("成长日记")
        if issue.title.startswith("202") and TABLE_DIR.get(issue.title[:4]):
            DIR = TABLE_DIR.get(issue.title[:4])
        check_dir( DIR["dir"])
        check_dir( DIR["img"])
        save_issue(issue, me)
        add_issue_id(issue.number)
        init_archives_table_readme()


template = '''---
pubDatetime: {}
title: {}
slug: {}'''

def download_image_file(url, file_name):
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)
        print(" # 写入DONE")
    return
def comp_url_down(url, path):
    import requests
    json_data = {
        'source': {
            'url': url,
        },
    }
    response = requests.post('https://api.tinify.com/shrink', headers={'Content-Type': 'application/json'}, json=json_data, auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    response = requests.get(response.json()["output"]["url"], auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    with open(path, 'wb') as f:
        f.write(response.content)

def replace_img_url(content, img_prefix):
    pattern = r'\((.*?)\)'
    matchs = re.findall(pattern, content)
    i = 0
    for img_url in matchs:
        if "github" in img_url:
            i = i + 1
            if (not os.path.exists(DIR["img"])):
                os.mkdir(DIR["img"])
            file_name = img_prefix +"-" + img_url.split('/')[-1] + ".jpg"
            comp_url_down(img_url, os.path.join(DIR["img"], file_name))
            content= content.replace('({})'.format(img_url), (DIR["ref_dir"]).format(file_name))
    return content

def add_cv(issue):
    cv = '''---
layout: ../layouts/ArchivesLayout.astro
title: ""
---'''
    md_name = "src/pages/cv.md"
    with open(md_name, "w", encoding="utf-8") as f:
        f.write(cv)
        f.write("\n\n")
        content = issue.body.replace('\r\n', "  \n")
        f.write(content or "")
def save_issue(issue, me):
    # 将datetime对象转为"北京时间"
    title = f"{issue.title.replace('/', '-').replace(' ', '.')}"
    if title == "关于我":
        add_cv(issue)
        return
    #  判断title是否包含时间
    dt = (issue.created_at + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    if title.startswith("202") and len(title) > 10 and title[0:10].count("-") == 2 and not dt.startswith(issue.title[0:10]):
        dt = title[0:10] + " " + dt[11:]
    temp = template.format(dt, title, title)
    md_name = os.path.join(
        DIR["dir"], f"{issue.title.replace('/', '-').replace(' ', '.')}.md"
    )
    labels = issue.labels
    with open(md_name, "w", encoding="utf-8") as f:
        f.write(temp)
        f.write("\n")
        if len(labels) > 0:
            f.write('''tags:\n''')
        for l in labels:
            f.write(f'- "{l.name}"\n')
        f.write("---\n")
        f.write("\n")
        # if not is_year:
        #     f.write(f"# [{issue.title}]({issue.html_url})\n\n")
        content = issue.body.replace('\r\n', "  \n")
        if IMG_SAVE_LOCAL and not (issue.milestone and issue.milestone.title == "no_save_image"):
            content = replace_img_url(content, dt[:10])
        f.write(content or "")
        if issue.comments:
            for c in issue.get_comments():
                if issue.user.login == me:
                    f.write("\n\n---\n\n")
                    dt = c.created_at + timedelta(hours=8)
                    f.write(dt.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    f.write(c.body or "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument(
        "--issue_number", help="issue_number", default=None, required=False
    )
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)