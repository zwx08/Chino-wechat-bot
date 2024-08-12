import os
import sys
import httpx
import requests

from Chino_old.plugins_parser import plugin_common
from Chino_old.model_definition import AnswerBase

class ip(plugin_common):


    __version__='0.0.1'
    @classmethod
    def main(cls,msg_l)-> AnswerBase | None:
        qu=msg_l["qu"]
        if qu.find("&ip") != -1:
            if len(qu) <= 4:
                try:
                    an = httpx.get('https://tbip.alicdn.com/api/queryip').text.strip()
                except:
                    an = "获取失败"
            else:
                an = cls.getting_ip(qu[4:])
            answer_model=AnswerBase(answer=an)
            return answer_model
        else:
            return None

    @staticmethod
    def getting_ip(args): #ip读取

        url = 'http://freeapi.ipip.net/' #中文免费
        url2 = 'http://ip-api.com/json/' #外国网站
        url=url+format(args)
        url2 = url2 + format(args)
        # response = httpx.get(url)
        response2 = httpx.get(url2)
        strpp=response2.json()  #把英文网站json接口返回值传给字典strpp


        return f"""您查询的IP地址:{args})
        <www.ip-api.com>
        国家:{strpp.get('country')}
        城市:{strpp.get('city')}
        经纬度坐标:{strpp.get('lat')},{strpp.get('lon')}
        运营商编号:{strpp.get('as')}
        ISP服务商:{strpp.get('isp')}"""