# coding=utf-8
import requests


class DingUtil:
    @staticmethod
    def notice_ding(title, content, link):
        json_data= {
            "actionCard": {
                "title": "简书："+title,
                "text": content,
                "btnOrientation": "0",
                "singleTitle" : "阅读全文",
                "singleURL" : link
            },
            "msgtype": "actionCard"
        }
        response = requests.post('https://oapi.dingtalk.com/robot/send?access_token=7fff5466a5711119b2059f1c65df3ab80c8a65025342f651c60c81618d9f4362', json=json_data)
        print(response.json())


if __name__ == '__main__':
    DingUtil.notice_ding("title", '''
    今天范哥家上周添了一闺女，要我去他们小区的家见识见识，上午起来和孩子去小学玩滑梯，还没玩一会儿，催着我回去去他哥家，在地下车库，问道这车位多少钱，她说8万多，我说比车都贵了，然后她就跟我争，8万都不算钱，呵，看自己是多能赚钱，昨天去宝龙就因为我没给她时间去买衣服生气，也可能是因为我把卖安全座椅的400要来生气，整个人就是个炸药桶，昨晚没做成，今天才知道是跟我爸要我给的10万块，没要出来跟我生气呢，哈哈哈我可真聪明，下午孩子醒了，我独自带着去河堤玩，以后再也不和你有关系了，孩子你想带着去哪儿玩，我就找理由不去，

就这么逼着我买小区，然后我提涨薪，不涨外出努力打工去吧，根本不考虑我感受，自私自利

  

![](https://upload-images.jianshu.io/upload_images/6904315-5882d9aec5f8dd47.jpg)  


    ''', "https://www.jianshu.com/p/9b35d22267ad")