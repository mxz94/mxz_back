# -*- coding: utf-8 -*-
import calendar
import mimetypes

import datetime

import argparse
import json
import os
import re
import requests
from datetime import timedelta
from github import Github

NOTE_DIR = "src/content/note"
NOTE_IMG = "public/img/note"

TABLE_DIR = {
    "note": {
        "img": "public/img/note",
        "dir": "src/content/note",
        "ref_dir": "(../../../public/img/note/{})"
        ,"mid": 13
    },
    "朝花夕拾": {
        "img": "public/img/zhxs",
        "dir": "src/content/blog/朝花夕拾",
        "ref_dir": "(../../../../public/img/zhxs/{})"
        ,"mid": 14
    },
    "成长日记": {
        "img": "public/img/czrj",
        "dir": "src/content/blog/成长日记",
        "ref_dir": "(../../../../public/img/czrj/{})"
        ,"mid": 15
    },
    "2024": {
        "img": "public/img/2024",
        "dir": "src/content/blog/2024",
        "ref_dir": "(../../../../public/img/2024/{})"
        ,"mid": 6
    },
    "2025": {
        "img": "public/img/2025",
        "dir": "src/content/blog/2025",
        "ref_dir": "(../../../../public/img/2025/{})"
        ,"mid": 7
    },
    "2026": {
        "img": "public/img/2026",
        "dir": "src/content/blog/2026",
        "ref_dir": "(../../../../public/img/2026/{})"
        ,"mid": 8
    },
    "2027": {
        "img": "public/img/2027",
        "dir": "src/content/blog/2027",
        "ref_dir": "(../../../../public/img/2027/{})"
        ,"mid": 9
    },
    "2028": {
        "img": "public/img/2028",
        "dir": "src/content/blog/2028",
        "ref_dir": "(../../../../public/img/2028/{})"
        ,"mid": 10
    },
    "2029": {
        "img": "public/img/2029",
        "dir": "src/content/blog/2029",
        "ref_dir": "(../../../../public/img/2029/{})"
        ,"mid": 11
    },
    "2030": {
        "img": "public/img/2030",
        "dir": "src/content/blog/2030",
        "ref_dir": "(../../../../public/img/2030/{})"
        ,"mid": 12
    }
}
DIR = TABLE_DIR["note"]

IMG_SAVE_LOCAL = True

class Article:
    def __init__(self, var1, var2, var3, var4, var5):
        self.pubDatetime = var1
        self.title = var2
        self.slug = var3
        self.tags = var4
        self.content = var5
def get_article_attrs(file_path:str):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        hasTag = False
        tags = []
        slug = None
        title = None
        content = ""
        startContent = False
        for line in lines:
            if startContent:
                content = content + line
                continue
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
                startContent = True
        content = content.replace('\n', '', 1)
        return Article(pubDatetime, title, slug, tags, content)
    except Exception as e:
        print(file_path)
def init_archives_table_readme():
    url = "https://blog.malanxi.top/blog/"
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
                title = file_name2.rsplit('.', 1)[0]
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
                title = file.rsplit('.', 1)[0]
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
            <div class="text-3xl w-full font-bold">日记</div>
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

def init_note_archives_table_readme():
    url = "https://blog.malanxi.top/note/"
    # 指定目录路径
    directory_path = "./src/content/note"
    article_url = '<li class="mt-3 mb-3"><a href="{}">{}</a></li>'
    # 使用os.listdir()获取目录下所有文件和文件夹的列表
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    m_d = {}
    file_list = sorted(file_list, key=lambda x: get_article_attrs(x).pubDatetime, reverse=True)
    for file in file_list:
        title = file.rsplit('.', 1)[0]
        article = get_article_attrs(file)
        if article.slug != None:
            title = article.slug
        month = article.pubDatetime[0:7]
        if m_d.get(month) is None:
            m_d[month] = []
        m_d[month].append(article_url.format(url + title, title, ))
#                 s[dir_name].append(article_url.format(url + u, title, ))
    start = '''---
    import BaseLayout from "../../../layouts/BaseLayout.astro";
    import TimeLineElement from "../../../components/cv/TimeLine.astro";
    ---

    <BaseLayout title="{}">
      <div class="mb-5">
        <div class="text-3xl w-full font-bold">笔记</div>
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
    file_path = "./src/pages/note/archives"
    tlist = []
    with open(file_path+"/notes.astro", 'w', encoding='utf-8') as file:
        for month, article in m_d.items():
            tlist.append(TimeLineElement.format(month, "\n".join(article)))
        file.write(start.format("notes", "\n".join(tlist)))

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
        init_note_archives_table_readme()


template = '''---
pubDatetime: {}
title: {}
slug: {}'''

def transfer_from_github_2_r2(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # 检查请求是否成功
    name = url.split('/')[-1]
    # 自动获取文件内容类型
    content_type = response.headers.get('content-type')
    if content_type:
        # 根据内容类型猜测文件扩展名
        extension = mimetypes.guess_extension(content_type.split(';')[0].strip())
    filename = name + extension
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    import boto3
    import datetime
    from botocore.config import Config

    # 令牌值 【令牌名称root_token】
    token = R2_TOKEN
    # 你的 Cloudflare R2 访问密钥和秘密密钥
    # 访问密钥 ID
    access_key = 'ad692e01f74450943b4122a84164835e'
    # 机密访问密钥
    secret_key = R2_KEY
    # 存储桶的 URL
    url = 'https://52666f83ef7dec7e1f33bc0afc91c693.r2.cloudflarestorage.com'


    # 创建一个 S3 客户端，这里指定了 R2 的端点
    config = Config(signature_version='s3v4')
    s3_client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=url,
        config=config
    )
    # 你要上传到存储桶的名字
    bucket_name = 'mxz'
    # 本地文件 文件名
    file_path = filename
    # 存储桶里的路径和文件名 此处可以重新命名上传后的文件名称，也可以添加文件夹
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    bucket_file_name = f'{year}/{filename}'
    # 使用 S3 客户端上传文件
    s3_client.upload_file(file_path, bucket_name, bucket_file_name)

    return "https://pub-4232cd0528364004a537285f400807bf.r2.dev/" + bucket_file_name

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


def calculate_new_size_from_url(image_url, target_width=None, target_height=None):
    from io import BytesIO
    from PIL import Image
    import requests
    # 通过网络请求获取图片
    response = requests.get(image_url)
    response.raise_for_status()  # 检查是否成功获取图片

    # 将内容转换为图片对象
    img = Image.open(BytesIO(response.content))

    # 获取原始分辨率
    original_width, original_height = img.size

    # 根据目标宽度或高度计算新尺寸
    if target_width is not None:
        ratio = target_width / original_width
        new_height = int(original_height * ratio)
        return target_width, new_height

    elif target_height is not None:
        ratio = target_height / original_height
        new_width = int(original_width * ratio)
        return new_width, target_height

    else:
        return original_width, original_height

def comp_url_down_new(url, path):
    import tinify
    tinify.key = "CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl"
    new_width, new_height = calculate_new_size_from_url(url, target_width=1200)
    source = tinify.from_url(url)
    resized = source.resize(
        method="fit",
        width=new_width,
        height=new_height
    )
    converted = resized.convert(type=["image/webp","image/png"])
    extension = converted.result().extension
    converted.to_file(path + "." + extension)
    # resized.to_file(path)
    return extension

def replace_img_url(content, img_prefix):
    pattern = r'\((.*?)\)'
    matchs = re.findall(pattern, content)
    i = 0
    for img_url in matchs:
        if "github" in img_url:
            i = i + 1
            if (not os.path.exists(DIR["img"])):
                os.mkdir(DIR["img"])
            file_name = img_prefix +"-" + img_url.split('/')[-1]
            # + ".jpg"
            extension = comp_url_down_new(img_url, os.path.join(DIR["img"], file_name))
            content= content.replace('({})'.format(img_url), (DIR["ref_dir"]).format(file_name + "." + extension))
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

def handle_video(content):
    lines = content.split("\n")
    for i in range(len(lines)):
        if lines[i].startswith("https://github.com/user-attachments"):
            url = transfer_from_github_2_r2(lines[i])
            # 使用响应式视频容器，去掉固定宽高
            video_html = f'''<div class="video-wrapper">
  <video src="{url}" controls controlsList="nodownload" preload="metadata" class="responsive-video">
    您的浏览器不支持视频播放
  </video>
</div>'''
            content = content.replace(lines[i], video_html)
    return content


def add_blog_to_typeco(md_name):
    data = get_article_attrs(md_name)
    data.content = data.content.replace("../../../public" if DIR["mid"] == 13 else "../../../../public", "https://blog.malanxi.top")
    img = None
    markdown_image_pattern = re.compile(r'!\[(.*?)\]\(([^)]+)\)')
    for match in markdown_image_pattern.finditer(data.content):
        img = match.group(2)  # 获取图片的 URL
        break
    try:
        dt = datetime.datetime.strptime(data.pubDatetime, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        dt = datetime.datetime.strptime(data.pubDatetime, '%Y-%m-%dT%H:%M:%SZ')
    timestamp = calendar.timegm(dt.timetuple())
    data = {
        "title": data.title,
        "str_value": img,
        "text": data.content,
        "mid": DIR["mid"],
        "created": timestamp
    }
    url = "https://pblog.malanxi.top/insert.php"
    response = requests.post(url, headers={"Content-Type": "application/json; charset=utf-8"}, data=json.dumps(data).encode('utf-8'))


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
        content = handle_video(content)
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

    add_blog_to_typeco(md_name)

R2_TOKEN = None
R2_KEY = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument("r2_token", help="r2_token")
    parser.add_argument("r2_key", help="r2_key")
    parser.add_argument(
        "--issue_number", help="issue_number", default=None, required=False
    )
    options = parser.parse_args()
    R2_TOKEN = options.r2_token
    R2_KEY = options.r2_key

    main(options.github_token, options.repo_name, options.issue_number)
