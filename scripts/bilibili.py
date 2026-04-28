import os
import time

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
def get_bilibili_video_info(page):
    import requests

    cookies = {
        'buvid3': '4C919E59-326B-F076-74C4-23468627D05038483infoc',
        'b_nut': '1757639438',
        '_uuid': '32EBE4BF-9F95-D5102-D761-F11945E10232438658infoc',
        'buvid_fp': '953fce15043f3f419a2548be0f46b864',
        'buvid4': '338DFC69-4765-B747-90B9-A4779E21642438060-023053117-AcLseL6ltuLpLPj0nhz7vQ%3D%3D',
        'rpdid': "|(kmYYlm)k0J'u~l~YJmRR|",
        'theme-tip-show': 'SHOWED',
        'enable_web_push': 'DISABLE',
        'theme-avatar-tip-show': 'SHOWED',
        'theme-switch-show': 'SHOWED',
        'DedeUserID': '2017895209',
        'DedeUserID__ckMd5': 'c5025633dc9fd7b9',
        'hit-dyn-v2': '1',
        'CURRENT_QUALITY': '80',
        'home_feed_column': '5',
        'CURRENT_FNVAL': '2000',
        'b_lsid': 'E107411107_19AB3A549A2',
        'browser_resolution': '1738-768',
        'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQyMDk3NDYsImlhdCI6MTc2Mzk1MDQ4NiwicGx0IjotMX0.GEvt-gL5QAWeVUYWlCwCT_PlN-5hxvxvvyn2yf7ecwE',
        'bili_ticket_expires': '1764209686',
        'SESSDATA': '9ad0d986%2C1779502548%2C052d2%2Ab1CjCjbEIJextYrP1lV3Q1uF8rpavfb29a0B-b6Sqvbn27kIY5fq5IFXCIdqts78iBWW0SVlVmcTNrMzdFT0wwUEdPcVhvU0FiaTZTZS1KcTF1eWp2V21nUWRBMU5rbXRYbFY2TlVHblMybE4zbzM0TVJTUG9PaWNmUGNRcDh0Vjc3SXpydnlZLTBRIIEC',
        'bili_jct': '3b8622fd92cf615d0a6a9a713bbdce47',
        'sid': 'djs28r5j',
        'bp_t_offset_2017895209': '1138648005432311808',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'priority': 'u=1, i',
        'referer': 'https://member.bilibili.com/platform/upload-manager/article?page=2',
        'sec-ch-ua': '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': "buvid3=4C919E59-326B-F076-74C4-23468627D05038483infoc; b_nut=1757639438; _uuid=32EBE4BF-9F95-D5102-D761-F11945E10232438658infoc; buvid_fp=953fce15043f3f419a2548be0f46b864; buvid4=338DFC69-4765-B747-90B9-A4779E21642438060-023053117-AcLseL6ltuLpLPj0nhz7vQ%3D%3D; rpdid=|(kmYYlm)k0J'u~l~YJmRR|; theme-tip-show=SHOWED; enable_web_push=DISABLE; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; DedeUserID=2017895209; DedeUserID__ckMd5=c5025633dc9fd7b9; hit-dyn-v2=1; CURRENT_QUALITY=80; home_feed_column=5; CURRENT_FNVAL=2000; b_lsid=E107411107_19AB3A549A2; browser_resolution=1738-768; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQyMDk3NDYsImlhdCI6MTc2Mzk1MDQ4NiwicGx0IjotMX0.GEvt-gL5QAWeVUYWlCwCT_PlN-5hxvxvvyn2yf7ecwE; bili_ticket_expires=1764209686; SESSDATA=9ad0d986%2C1779502548%2C052d2%2Ab1CjCjbEIJextYrP1lV3Q1uF8rpavfb29a0B-b6Sqvbn27kIY5fq5IFXCIdqts78iBWW0SVlVmcTNrMzdFT0wwUEdPcVhvU0FiaTZTZS1KcTF1eWp2V21nUWRBMU5rbXRYbFY2TlVHblMybE4zbzM0TVJTUG9PaWNmUGNRcDh0Vjc3SXpydnlZLTBRIIEC; bili_jct=3b8622fd92cf615d0a6a9a713bbdce47; sid=djs28r5j; bp_t_offset_2017895209=1138648005432311808",
    }

    params = {
        'status': 'is_pubing,pubed,not_pubed',
        'pn': str(page),
        'ps': '10',
        'coop': '1',
        'interactive': '1',
    }

    response = requests.get('https://member.bilibili.com/x/web/archives', params=params, cookies=cookies, headers=headers)
    return response.json()['data']['arc_audits']

def vis(aid):
    import requests

    cookies = {
        'buvid3': '4C919E59-326B-F076-74C4-23468627D05038483infoc',
        'b_nut': '1757639438',
        '_uuid': '32EBE4BF-9F95-D5102-D761-F11945E10232438658infoc',
        'buvid_fp': '953fce15043f3f419a2548be0f46b864',
        'buvid4': '338DFC69-4765-B747-90B9-A4779E21642438060-023053117-AcLseL6ltuLpLPj0nhz7vQ%3D%3D',
        'rpdid': "|(kmYYlm)k0J'u~l~YJmRR|",
        'theme-tip-show': 'SHOWED',
        'enable_web_push': 'DISABLE',
        'theme-avatar-tip-show': 'SHOWED',
        'theme-switch-show': 'SHOWED',
        'DedeUserID': '2017895209',
        'DedeUserID__ckMd5': 'c5025633dc9fd7b9',
        'hit-dyn-v2': '1',
        'CURRENT_QUALITY': '80',
        'home_feed_column': '5',
        'browser_resolution': '1738-768',
        'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQyMDk3NDYsImlhdCI6MTc2Mzk1MDQ4NiwicGx0IjotMX0.GEvt-gL5QAWeVUYWlCwCT_PlN-5hxvxvvyn2yf7ecwE',
        'bili_ticket_expires': '1764209686',
        'SESSDATA': '9ad0d986%2C1779502548%2C052d2%2Ab1CjCjbEIJextYrP1lV3Q1uF8rpavfb29a0B-b6Sqvbn27kIY5fq5IFXCIdqts78iBWW0SVlVmcTNrMzdFT0wwUEdPcVhvU0FiaTZTZS1KcTF1eWp2V21nUWRBMU5rbXRYbFY2TlVHblMybE4zbzM0TVJTUG9PaWNmUGNRcDh0Vjc3SXpydnlZLTBRIIEC',
        'bili_jct': '3b8622fd92cf615d0a6a9a713bbdce47',
        'CURRENT_FNVAL': '4048',
        'sid': 'eelw3wgp',
        'b_lsid': 'E3D735108_19AB4E810F0',
        'bp_t_offset_2017895209': '1138740849740349440',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://member.bilibili.com',
        'priority': 'u=1, i',
        'referer': 'https://member.bilibili.com/platform/upload-manager/article?group=pubed&page=4',
        'sec-ch-ua': '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0',
        # 'cookie': "buvid3=4C919E59-326B-F076-74C4-23468627D05038483infoc; b_nut=1757639438; _uuid=32EBE4BF-9F95-D5102-D761-F11945E10232438658infoc; buvid_fp=953fce15043f3f419a2548be0f46b864; buvid4=338DFC69-4765-B747-90B9-A4779E21642438060-023053117-AcLseL6ltuLpLPj0nhz7vQ%3D%3D; rpdid=|(kmYYlm)k0J'u~l~YJmRR|; theme-tip-show=SHOWED; enable_web_push=DISABLE; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; DedeUserID=2017895209; DedeUserID__ckMd5=c5025633dc9fd7b9; hit-dyn-v2=1; CURRENT_QUALITY=80; home_feed_column=5; browser_resolution=1738-768; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQyMDk3NDYsImlhdCI6MTc2Mzk1MDQ4NiwicGx0IjotMX0.GEvt-gL5QAWeVUYWlCwCT_PlN-5hxvxvvyn2yf7ecwE; bili_ticket_expires=1764209686; SESSDATA=9ad0d986%2C1779502548%2C052d2%2Ab1CjCjbEIJextYrP1lV3Q1uF8rpavfb29a0B-b6Sqvbn27kIY5fq5IFXCIdqts78iBWW0SVlVmcTNrMzdFT0wwUEdPcVhvU0FiaTZTZS1KcTF1eWp2V21nUWRBMU5rbXRYbFY2TlVHblMybE4zbzM0TVJTUG9PaWNmUGNRcDh0Vjc3SXpydnlZLTBRIIEC; bili_jct=3b8622fd92cf615d0a6a9a713bbdce47; CURRENT_FNVAL=4048; sid=eelw3wgp; b_lsid=E3D735108_19AB4E810F0; bp_t_offset_2017895209=1138740849740349440",
    }

    params = {
        'csrf': '3b8622fd92cf615d0a6a9a713bbdce47',
    }

    data = {
        'aid': aid,
        'is_only_self': '0',
        'csrf': '3b8622fd92cf615d0a6a9a713bbdce47',
    }

    response = requests.post(
        'https://member.bilibili.com/x/vu/web/edit/visibility',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    print(response.json())
if __name__ == '__main__':

    for page in range(3, 33):
        info = get_bilibili_video_info(page)
        for ite in info:
            try:
                print(ite["Archive"]["aid"])
                vis(ite["Archive"]["aid"])
                # time.sleep(2)
            except:
                pass
