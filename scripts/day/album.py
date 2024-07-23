import json

from scripts.utils.aligo_utils import CustomAligo
from scripts.utils.file_utils import FileUtils

aligo = CustomAligo()
list = aligo.list_all_files(album_id='bAW9TKuLxDk')
data = []
for file in list:
    m = file.image_media_metadata
    ad = m.address_line
    date = m.time
    url = file.thumbnail
    data.append({
        'address': ad,
        'time': date,
        'src': url
    })

FileUtils.write_json("images.json", data)
