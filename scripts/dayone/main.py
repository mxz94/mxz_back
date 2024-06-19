import os
import re
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

import jsonschema
import ujson


def validate_schema(data):
    return jsonschema.validate(data)


def process_timestamp(timestamp: str) -> str:
    d = datetime.utcfromtimestamp(timestamp)
    formatted_timestamp = d.strftime(Config.datetime_format)


    return formatted_timestamp


def process_tags(text: str) -> List:
    tags = re.findall("#[a-z]+", text)

    for tag in tags:
        text = text.replace(tag, '')


    return text, [t[1:]for t in tags]


def generate_uuid() -> str:
    return uuid.uuid4().hex.upper()


def process_photos(text: str, ctime: str) -> str:
    """
    Find all regex matches of image patterns
    Iterate over each one of them and update the text in the dayone format

    Args:
        text (str): Original text where we need to search for image regex

    Returns:
        (str): Modified text replaced with compatible format
    """
    pattern = r'\((.*?)\)'

    matches = re.findall(pattern, text)
    processed_imgs = []

    if matches:

        # For each match of the image in a line of text
        for idx, match in enumerate(matches):
            # Find out the format of the image
            photo_frmt = None
            for frmt in Config.formats:
                if len(match.split(frmt)) > 1:
                    (path, fileName) = os.path.split(match)
                    match = fileName
                    # try:
                    #     shutil.copy('./img/{}'.format(fileName), './photos/{}'.format(fileName))
                    # except Exception as e:
                    #     print(1)
                    photo_frmt = frmt
                    global id
                    id = re.sub(r'!(\[.)', '', match.split(frmt)[0])
                    break
            if photo_frmt is not None:
                photo = dict(
                    orderInEntry=idx,
                    creationDevice=CreationConfig.creationDevice,
                    date=ctime,
                    identifier=id,
                    md5=id,
                    type=photo_frmt.replace('.', ''),
                    isSketch=False,
                )

                processed_imgs.append(photo)

                text = Config.dayone_image.format(image_name=id)

    return text, processed_imgs


def process_text(text: str, ctime: str) -> str:
    """
    Process markdown text and return it in compatible format

    Args:
        text (str): Original text

    Returns:
        str: Processed text

    8ui*9x9ZirAFGS
    """

    lines = re.split("\n+", text)
    processed_lines, processed_imgs = [], []

    # Process line by line
    for line in lines:
        response = process_photos(line, ctime)
        processed_lines.append(response[0])
        processed_imgs += response[1]

    return '\n'.join(processed_lines), processed_imgs

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

def process_file(file: os.DirEntry) -> dict:
    """
    Processes a single markdown file and convert it into Day One format

    Args:
        file (os.DirEntry): File type

    Returns:
        dict: DayOne format dict
    """
    aricle = get_article_attrs(file)
    text = ""
    with open(file, 'r', encoding='utf-8') as f:
        i = 0
        for line in f:
            if i == 2:
                text = text + line
            if line.startswith("---"):
                i = i + 1
    try:
        try:
            if aricle.pubDatetime.startswith(file.name[0:10]):
                time = (datetime.strptime(aricle.pubDatetime.replace('\n','' ),  "%Y-%m-%d %H:%M:%S") - timedelta(hours=8)).isoformat()
            else:
                time = (datetime.strptime(file.name[0:10], "%Y-%m-%d") - timedelta(hours=8)).isoformat()
        except Exception as e:
            time = (datetime.strptime(file.name[0:10], "%Y-%m-%d") - timedelta(hours=8)).isoformat()
    except Exception as e:
        time = datetime.isoformat(datetime.now())
    text = file.name.replace('.md', '') + '\n' + text
    text, tags = process_tags(text)
    text, photos = process_text(text, time)

    tags.append("sz")
    #TODO: Generate schema automatically
    entry = {}
    entry.update({
        "tags": tags,
        "uuid": generate_uuid(),
        "starred": False, #TODO: Take user input for starred files
        "creationOSName": CreationConfig.creationOSName,
        "timeZone": Config.timeZone,
        "photos": photos,
        "text": text,
        "creationDate": time,
        "creationDeviceType": CreationConfig.creationDeviceType,
        "modifiedDate": time,
        "location" : {
            "region" : {
                "center" : {
                    "longitude" : 112.46752499999999,
                    "latitude" : 34.601416999999998
                },
                "identifier" : "<+34.60141700,+112.46752500> radius 197.28",
                "radius" : 197.28449957851379
            },
            "localityName" : "洛阳市",
            "country" : "中国",
            "timeZoneName" : "Asia\/Shanghai",
            "administrativeArea" : "河南省",
            "longitude" : 112.46794128417969,
            "placeName" : "伊洛路110号",
            "latitude" : 34.601852416992188
        }
    })

    #TODO: Validate schema
    # if validate_schema(entry):
    #     print("ERROR: Not able to validate the schema!")

    return entry


def convert_md(source:str) -> dict:
    print(f"\n\n-----\nProcessing folder: {source}\n-----\n\n")
    entries, sub_folders = [], []

    with os.scandir(source) as dir_contents:
        # Process directory contents one after the other
        for entry in dir_contents:

            if entry.name.startswith('.'):
                continue

            if entry.is_file() and entry.name.split(".")[-1] == "md":

                data = process_file(entry)

                if data is not None:
                    entries.append(data)
                    continue

                continue

            elif entry.is_file() and entry.name.split(".")[-1] != "md":
                continue

            sub_folders.append(entry)

    for folder in sub_folders:
        temp = convert_md(folder)
        entries += temp
    print(entries.__len__())
    return entries

@dataclass
class Config:
    """
    Generic config for entries in DayOne
    """
    datetime_format: str = "%Y-%m-%dT%H:%M:%S%Z"
    timeZone: str = "Asia\/Shanghai"
    # Regex that is used to find images in markdown. Currently this is compatible with Obsidian.
    image_regex = re.compile(r'(!\[\[.*?\]\])')
    # DayOne replacement text
    dayone_image = '![](dayone-moment://{image_name})'
    formats = ['.jpeg', '.png', '.jpg']


@dataclass
class LoggingConfig:
    """
    Logging configs
    """
    logger_format = '["%(levelname)s"] module: %(module)s func_name: %(funcName)s line: %(lineno)s \t "%(message)s"'
    logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        root={
            "level": "INFO",
            "handlers": ["app"]
        },
        formatters={
            "app": {
                "format": str(logger_format),
                "class": "logging.Formatter"
            }
        },
        handlers={
            "app": {
                "class": "logging.StreamHandler",
                "formatter": "app",
                "stream": "ext://sys.stdout"
            }
        }
    )


@dataclass
class CreationConfig:
    """
    Config for creation device
    """
    creationOSName: str = 'IOS'
    creationDeviceType: str = 'Iphone 14 plus'
    creationDevice: str = 'Iphone 14 plus'


def compress_files_and_folders(zip_filename, files, folders):
    """
    压缩指定的文件和文件夹到ZIP文件中。

    :param zip_filename: str, ZIP文件的输出路径及名称。
    :param files: list, 单个文件的路径列表。
    :param folders: list, 要压缩的文件夹路径列表。
    """
    from zipfile import ZipFile
    with ZipFile(zip_filename, 'w') as zipf:
        # 添加文件
        for file in files:
            if os.path.isfile(file):
                zipf.write(file, os.path.basename(file))

        # 压缩文件夹及其内容
        for root, dirs, filenames in os.walk(folders):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                zipf.write(file_path, file_path)

def delete_all_files(folder_path):
    # 获取文件夹中所有文件的列表
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        # 判断是否为文件
        if os.path.isfile(file_path):
            # 删除文件
            os.remove(file_path)



def replace_img_url(file):
    content = ""
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        # i = 0
        # for line in f:
        #     if i == 2:
        #         content = content + line
        #     if line.startswith("---"):
        #         i = i + 1
    pattern = r'\((.*?)\)'
    matchs = re.findall(pattern, content)
    i = 0
    for img_url in matchs:
        if img_url.endswith(".jpg") or img_url.endswith(".png") or img_url.endswith(".jpeg"):
            img = img_url.split("public")[-1]
            print(img)
            shutil.copy2("../../public" + img, "./photos")
            content = content.replace(img_url, "photos/" + img.split("/")[-1])
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

def move_md(path, start):
    l = os.listdir(path)
    l = [i for i in l if i > start and i.startswith(start[:5])]

    # copy 文件
    for i in l:
        shutil.copy2(os.path.join(path, i), os.path.join("md", i))
        replace_img_url(os.path.join("md", i))

path= r"../../src/content/blog/2024"
import_start = "2024-05-26"

if __name__ == '__main__':
    move_md(path, import_start)

    entries = {
        "entries": convert_md(source =r"./md")
    }
    with open(os.path.join('./', "day_one_import.json"), "w", encoding="utf-8") as fp:
        ujson.dump(entries, fp, escape_forward_slashes=False, ensure_ascii=False)

    # 压缩到指定的ZIP文件
    output_zip = 'day_one_import.zip'
    compress_files_and_folders(output_zip, ['day_one_import.json'], './photos')

    # 删除文件
    delete_all_files("./md")
    os.remove("day_one_import.json")
    delete_all_files("./photos")