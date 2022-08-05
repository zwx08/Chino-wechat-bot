import os
import sys
import httpx

from action_sql import *


def getting_ip(args): #ip读取
    url = 'http://freeapi.ipip.net/' #中文免费
    url2 = 'http://ip-api.com/json/' #外国网站
    url=url+format(args)
    url2 = url2 + format(args)
    response = httpx.get(url)
    response2 = httpx.get(url2)
    
    str=response.text.replace('\"','') #去掉双引号
    str=str.replace('[','')      #去掉方括号
    str=str.replace(']','')
    str=str.replace(' ','')
    
    str=str.split(",")  #已逗号为分割符号，分割字符串为数组
    str[4] = str[4].replace('\n', '') #去掉回车符号

    strpp={}         #定义一个字典strpp
    strpp=response2.ujson()  #把英文网站json接口返回值传给字典strpp


    return f"""您查询的IP地址:{args})
    <www.ipip.net>
    国家:{str[0]}
    省份:{str[1]}
    城市:{str[2]}
    区域:{str[3]}
    运营商:{str[4]}"
    <www.ip-api.com>
    国家:{strpp.get('country')}
    城市:{strpp.get('city')}
    经纬度坐标:{strpp.get('lat')},{strpp.get('lon')}
    运营商编号:{strpp.get('as')}
    ISP服务商:{strpp.get('isp')}"""
    
def start(l):
    qu=l["qu"]
    if len(qu) <= 4:
        an = httpx.get('https://checkip.amazonaws.com').text.strip()
    else:
        an = getting_ip(qu[4:])
    return an

if __name__ =='__main__':
    #插件信息写入
    print("加载插件ip...")
    plugins_sql.inf(os.path.basename(__file__),0.01,"zwx08","ip查询")
    qu_key.write("ip","&ip",1,"plugins.ip.start",1,"ip查询")