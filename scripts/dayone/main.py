import argparse
import logging.config
import os

import ujson

from scripts.dayone.config import LoggingConfig
from scripts.dayone.file_converter import convert_md

logger = logging.getLogger()
logging.config.dictConfig(LoggingConfig.logging_config)

if __name__ == '__main__':
    """
    python3 --source <> --dest <>
    --debug y # To generate logs
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--source',
        help='Location of the file or folder which you want to convert. If you pass the folder location, all files present will be converted',
        type=str,
        default=None,
        required=True
    )

    parser.add_argument(
        '--dest',
        help='Location of the folder where you want to dump the converted notes in JSON format. Defaults to the current working directory.',
        type=str,
        default=os.path.join(os.getcwd()),
        required=False
    )

    parser.add_argument(
        '--debug',
        help='Weather to run in debug mode (y/n). Defaults to `n`',
        type=str,
        default='n',
        required=False
    )


    logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    entries = {
        "entries": convert_md(source = r'D:\markdown-to-dayone\ri')
    }

    with open(os.path.join('/', "day_one_import.json"), "w", encoding="utf-8") as fp:
        ujson.dump(entries, fp, escape_forward_slashes=False, ensure_ascii=False)
