from datetime import datetime
import os
from logging import getLogger
from .utils import (
    process_text,
    process_tags,
    process_timestamp,
    generate_uuid
)
from .config import (
    Config,
    CreationConfig
)

logger = getLogger()

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
    time = datetime.strptime(file.name[0:10], "%Y-%m-%d").isoformat()
    file_sats = file.stat()
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
                logger.info(f"Skipping hidden file/folder: {entry.name}")
                continue

            if entry.is_file() and entry.name.split(".")[-1] == "md":
                logger.info(f"Processing {entry.name}")

                data = process_file(entry)

                if data is not None:
                    logger.info(f"Completed processing for {entry.name}")
                    entries.append(data)
                    continue

                logger.error(f"Not able to process {entry.name}")
                continue

            elif entry.is_file() and entry.name.split(".")[-1] != "md":
                logger.info(f"Non markdown file found {entry.name}")
                continue

            logger.debug(f"Subfolder found {entry.name}")
            sub_folders.append(entry)

    logger.debug(f"Sub folders: {sub_folders}")
    for folder in sub_folders:
        temp = convert_md(folder)
        entries += temp
    print(entries.__len__())
    return entries
