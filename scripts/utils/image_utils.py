import os

import requests


def download_image_file(url, file_name):
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)
        print(" # 写入DONE")

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
def comp_path(path):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    with open(path, 'rb') as f:
        data = f.read()

    response = requests.post('https://api.tinify.com/shrink', headers=headers, data=data, auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    return response.json()["output"]["url"]

def down_com_img(url, path):
    response = requests.get(url, auth=('api', 'CvLpLgG3f9RffKkYdV3kqrTCxhzSHxQl'))
    with open(path, 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    for f in os.listdir(r"D:\mxz\mxz_back\public\img\zhxs"):
        p = os.path.join(r"D:\mxz\mxz_back\public\img\zhxs", f)
        down_com_img(comp_path(p), p)
