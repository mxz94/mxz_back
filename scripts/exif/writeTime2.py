import os

a = r'''

Exiftool.exe -r -api "QuickTimeUTC" "-CreateDate={date}" "{path}"

Exiftool.exe -r -api "QuickTimeUTC" "-MediaCreateDate={date}" "{path}"

Exiftool.exe -r -api "QuickTimeUTC" "-TrackCreateDate={date}" "{path}"
'''


a = a.replace('{date}', "2020:08:01 00:00:00").replace("{path}", r"D:\tmp\p\2020\Camera")

with open(r"C:\Program Files\Metadata++\run.bat", "w", encoding="utf8") as f:
    f.write(a);