import requests

headers = {
    'Referer': '',
    'Authorization': 'Bearer sk-123123123456',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Content-Type': 'application/json',
}

json_data = {
    'model': 'gpt-3.5-turbo',
    'messages': [
        {
            'role': 'user',
            'content': 'You are a helpful assistant that summarize video subtitle.\nSummarize in language \'中文简体\'.\nAnswer in markdown json format.\n\nexample output format:\n\n```json\n{\n  "summary": "brief summary"\n}\n```\n\nThe video\'s title: \'\'\'关于我爸成了全班人义父那件事\'\'\'.\nThe video\'s subtitles:\n\n\'\'\'\n走读生最早的外卖员来我的鸡蛋灌饼,小红米的快递,又我的输出完了还泡面,奶茶,还搭了一碗,干嘛,回去多少钱,还有书包,没这么大显眼猫,好耶,你家俩人话,小宝贝12341路冲过来,手机哈哈头发老板包子,我的最爱头发了,100块头发了,哇我的漂亮妈妈,你放过一个啊,我的手机欧巴,鸡蛋灌饼都给我拿出来,不要乱抱我,高中同学们,英的哈哈哈哈哈,真实乔宇班级吗,乔宇向我的办公室配老师,这我的对不起,都书包门口搞笑,记得关门啊哈啊小说肉,你的不加不加酸菜啊,还有王允许飞了,小明,你什么都不加不,张杰你的加速吃,乐天义父,脱单义父,他们嘴里面我的评论他干嘛,你爸呢包子来没来,如来来\n\'\'\'',
        },
    ],
    'temperature': 0,
    'n': 1,
    'stream': False,
}

response = requests.post('http://127.0.0.1:8080/v1/chat/completions', headers=headers, json=json_data)
print(response.json())