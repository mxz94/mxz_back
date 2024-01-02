from scripts.utils.file_utils import FileUtils

src = r"D:\mxz\mxz_back\src\content\blog"
i = 0
for file in FileUtils.read_all_file(src):
    l = []
    with open(file, "r", encoding="utf8") as f:
        l = f.readlines()
        if l[2].startswith("title"):
            l.insert(3, l[2].replace("title", "slug"))
    if (l.__len__() < 4):
        print(file)
    with open(file, "w", encoding="utf8") as f:
        f.writelines(l)

