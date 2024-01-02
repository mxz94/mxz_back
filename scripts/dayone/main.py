import os
import shutil
import uuid
import zipfile
from typing import List

import jsonschema
import pyzipper
import ujson
import re
from dataclasses import dataclass
from datetime import datetime

def validate_schema(data):
    return jsonschema.validate(data)


def process_timestamp(timestamp: str) -> str:
    d = datetime.utcfromtimestamp(timestamp)
    formatted_timestamp = d.strftime(Config.datetime_format)


    return formatted_timestamp


def process_tags(text: str) -> List:
    """
    Process the text and returns a list of all tags in the Markdown text

    Arguments:
        - text {str} -- Markdown text
    Returns:
        - {list} -- List of all tags
    """
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
                print(match)
                if len(match.split(frmt)) > 1:
                    (path, fileName) = os.path.split(match)
                    match = fileName
                    try:
                        shutil.copy('./img/{}'.format(fileName), './photos/{}'.format(fileName))
                    except Exception as e:
                        print(1)
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

                text = text.replace(
                    match,
                    Config.dayone_image.format(image_name=id)
                )


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

def process_file(file: os.DirEntry) -> dict:
    """
    Processes a single markdown file and convert it into Day One format

    Args:
        file (os.DirEntry): File type

    Returns:
        dict: DayOne format dict
    """
    with open(file, "r", encoding='utf-8') as fp:
        text = fp.read()
    print(file.name)
    try:
        time = datetime.strptime(file.name[0:10], "%Y-%m-%d").isoformat()
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
    """
    Converts all the files in a particular folder to JSON format that can be imported by Day One

    Args:
        source (str): Source folder where the markdown files are present

    Returns:
        dict: Dict that can be written to disk (expected by Day One)
    """

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
    timeZone: str = "IST"
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

def encrypt_zip_folder(folder_path, zip_file_path, password):
    # 创建一个新的 ZIP 文件
    oneName = "E:\\" + fileName
    twoName = zip_file_path + "\\" + fileName

    with pyzipper.AESZipFile(oneName, 'w', compression=zipfile.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
        # 设置 ZIP 文件的密码
        zipf.setpassword(password.encode())

        # 遍历文件夹中的所有文件和子文件夹
        for root, _, files in os.walk(folder_path):
            for file in files:
                # 获取文件的完整路径
                file_path = os.path.join(root, file)
                # 将文件添加到 ZIP 压缩文件中，第二个参数是保存到 ZIP 文件中的相对路径
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    with pyzipper.AESZipFile(twoName, 'w', compression=zipfile.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
        # 设置 ZIP 文件的密码
        # zipf.setpassword(password.encode())
        zipf.write(oneName)

src = r"./"

if __name__ == '__main__':

    entries = {
        "entries": convert_md(source =src)
    }

    with open(os.path.join('./', "day_one_import.json"), "w", encoding="utf-8") as fp:
        ujson.dump(entries, fp, escape_forward_slashes=False, ensure_ascii=False)
