import re

from scripts.utils.file_utils import FileUtils
# /img/, "/../../public/img/"

src = r"D:\mxz\mxz_back\src\content\blog2"
i = 0

def replace_img_url(content):
    pattern = r'\((.*?)\)'
    matchs = re.findall(pattern, content)
    for img_path in matchs:
        if img_path.endswith(".jpeg") or img_path.endswith(".jpg") or img_path.endswith(".png"):
            return "/public/img" + img_path.split("img")[1]
    return None
s = {}
for file in FileUtils.read_all_file(src):
    with open(file, "r", encoding="utf8") as f:
        content = f.read()
        img = replace_img_url(content)
        if img:
            s[file] = img

for item in s.items():
    # if 'heroImage: "{}"'.format(item[1]).__eq__('heroImage: "/public/img/"'):
    #     print(item)
    l = []
    with open(item[0], "r", encoding="utf8") as f:
        l = f.readlines()
        if l[2].startswith("title"):
            l.insert(3, 'heroImage: "{}"\n'.format(item[1]))
    if (l.__len__() < 4):
        print(file)
    with open(item[0], "w", encoding="utf8") as f:
        f.writelines(l)



# /img/, "/../../public/img/"