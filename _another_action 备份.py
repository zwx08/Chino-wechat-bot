#自设字符转换:此例子使用_a_作为字符转换，an例子:_a_好~
#随机图片注意:文件夹中文件格式必须为微信支持图片格式,且不得有乱码文件，部分在action.py中有写，如果有其他微信支持扩展名（比如jpeg)，请按照action中格式添加到action.py
#自设字符转换
from distutils.log import error
from more_action import *
import httpx,ujson,sys,json
from sympy import *
import yaml
from file_action import *

def nickname(port,wxid_group):
    #update_group_member_details(port,wxid,wxid_group)
    wxid_de=get_wxid_details(port,wxid_group)
    nickname=wxid_de["data"]["nickName"]
    return nickname
def wxid_form_cr(wxid,sender):
    if "@chatroom" in wxid:
        cda=get_chatroom_details_all(wxid)
        for x in cda['data']:
            if x["NickName"] == sender or x["Alias"] == sender or x["RoomNick"] == sender:
                return x["UserName"]
    else:
        print("Error for wxid is must be chatroom(wxid_form_cr)")
        return 
def wxid_form_nickname_cr(port,wxid,nickname):
    if "@chatroom" in wxid:
        cda=get_chatroom_details_all(wxid)
        for x in cda['data']:
            if x["NickName"] == nickname:
                return x["UserName"]
    else:
        print("Error for wxid is must be chatroom(wxid_form_nickname_cr)")
        return None

def wxid_form_Alias_cr(wxid,Alias):
    if "@chatroom" in wxid:
        cda=get_chatroom_details_all(wxid)
        for x in cda['data']:
            if x["Alias"] == Alias:
                return x["UserName"]
    else:
        print("Error for wxid is must be chatroom(wxid_form_Alias_cr)")
        return None
def wxid_form_RoomNick_cr(wxid,RoomNick):
    if "@chatroom" in wxid:
        cda=get_chatroom_details_all(wxid)
        for x in cda['data']:
            if x["RoomNick"] == RoomNick:
                return x["UserName"]
    else:
        print("Error for wxid is must be chatroom(wxid_form_RoomNick_cr)")
        return None

class call:
    def data_name_write(name_write,name_write_call):
        data=data_read()
        with open('wx_data.json', 'w', encoding='utf-8') as file:
            data["wx_name"][name_write]=name_write_call
            data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
            file.write(data_json)
            file.close()

    def _a_ (an,wxid,wxid_group,port):
        if an.find('_a_') != -1 :
            data=data_read()
            wx_name=data["wx_name"]
            if wxid_group:
                wxid=wxid_group

                #    print(wx_name[wxid])
                if wxid in wx_name:
                    anr=an.replace('_a_',wx_name[wxid])

                #        print("有",anr)
                else:
                    #update_group_member_details(port,wxid,wxid_group)
                    wxid_de=get_wxid_details(port,wxid_group)
                    nickname=(wxid_de["data"])["nickname"]
                    print(nickname)
                    anr=an.replace('_a_',nickname)
                #        print('无')
                return anr
        else:
            return an

    def name_write(qu,wxid,port):
        qu_data=qu.splitlines()
        get_chatroom_details_all(wxid)
        if qu_data[1][:3] == "wxid":
            wxid=qu_data[1]
        else:
            wxid=wxid_form_nickname_cr(port,wxid,qu_data[1])
        if wxid==None:
            return "error"
        call.data_name_write(wxid,qu_data[2])


    def read_name_all():
        data=data_read()
        data_json=ujson.dumps(data["wx_name"], ensure_ascii=False, indent=4)
        return data_json


class warn:
    def data_warn_write(wxid,sender,t):
        data=data_read()
        if wxid in data["wx_warn"]:
            if sender in data["wx_warn"][wxid]:
                data["wx_warn"][wxid][sender] += t
            else:
                data["wx_warn"][wxid][sender] = t
        else:
            data["wx_warn"][wxid] = {}
            data["wx_warn"][wxid][sender] = t
        with open('wx_data.json', 'w', encoding='utf-8') as file:
            data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
            file.write(data_json)
            file.close()
        return data["wx_warn"][wxid][sender]



    def warn(qu,port,wxid):
        qu_data=qu.splitlines()
        if len(qu_data[0]) > 6:
            t=qu_data[0][6:]
        else:
            t=1
        sender=qu_data[1]
        if qu_data[1][:3] != "wxid":
            wxi=wxid_form_cr(wxid,sender)
            if wxi==None:
                return "error_wfc"
            
        elif qu_data[1][:3] == "wxid":
            wxi=sender
        time=warn.data_warn_write(wxid,wxi,int(t))
        #name=_a_ ("_a_",qu_data[1],qu_data[1],port)
        if 	len(qu_data) == 3:
            return f"警告:{nickname(port,wxi)}-{wxi}({wxid}:{time}/16)\n原因:{qu_data[2]}"
        else:
            return f"警告:{nickname(port,wxi)}-{wxi}({wxid}:{time}/16)"

    def w_all(wxid):
        data=data_read()
        data_json=ujson.dumps(data["wx_warn"][wxid], ensure_ascii=False, indent=4)
        return data_json
    def w_all_all():
        data=data_read()
        data_json=ujson.dumps(data["wx_warn"], ensure_ascii=False, indent=4)
        return data_json
    def w_del(qu,wxid):
        qu_data=qu.splitlines()
        if len(qu[0]) >7:
            wxid=qu[0][7:]
        for x in qu_data[1:]:
            if x[:3] != "wxid":
                wxi=wxid_form_cr(wxid,x)
                if wxi==None:
                    return "error_wfc"
        data=data_read()
        del data["wx_warn"][wxid][wxi]
        data_write_data(data)
        data=data_read()
        if wxi not in data["wx_warn"][wxid]:
            return "success"
        else:
            return "error"
        
class another_data_write:
    def admin(qu):
        qu_data=qu.splitlines()
        data=data_read()
        data["wxid_admin"].extend(qu_data[1:])
        data["wxid_admin"]=list(set(data["wxid_admin"]))
        data_write_data(data)
        data=data_read()
        d = [False for c in qu_data[1:] if c not in data["wxid_admin"]]
        if d:
            return 'error'
        else:
            return 'success'
    
    def block(qu):
        qu_data=qu.splitlines()
        data=data_read()
        data["wxid_block"].extend(qu_data[1:])
        data["wxid_block"]=list(set(data["wxid_block"]))
        data_write_data(data)
        data=data_read()
        d = [False for c in qu_data[1:] if c not in data["wxid_block"]]
        if d:
            return 'error'
        else:
            return 'success'
        
    def white(qu):
        qu_data=qu.splitlines()
        data=data_read()
        data["wxid_white"].extend(qu_data[1:])
        data["wxid_white"]=list(set(data["wxid_white"]))
        data_write_data(data)
        d = [False for c in qu_data[1:] if c not in data["wxid_white"]]
        if d:
            return 'error'
        else:
            return 'success'
    
#随机图片
def image():
    import os
    import random

    rootdir = "X:\Web\pixiv" #更改为你自己放图片的文件夹
    file_names = []
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数:分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        file_names = filenames
        # for filename in filenames:                        #输出文件信息
        #     print("parent is" + parent)
        #     print("filename is:" + filename)
        #     print("the full name of the file is:" + os.path.join(parent, filename))
    x = random.randint(0, len(file_names)-1)
    image=rootdir+"\\"+file_names[x]  
    return image

def getting_ip(argv):
    url = 'http://freeapi.ipip.net/' #中文免费
    url2 = 'http://ip-api.com/json/' #外国网站
    args = argv
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


class sympy:
    x, y, z ,a ,b= symbols('x y z a b')
    


def pixiv():
#pixiv作品推荐
#    from pixivpy3 import *
    from gppt import GetPixivToken
    g = GetPixivToken()
    res = g.login(headless=True, user="zwx.08@qq.com", pass_="zwx20080104")
    print(res)
#    aapi = AppPixivAPI()
#    json_result = aapi.illust_recommended()
#    print(json_result)
#    illust = json_result.illusts[0]
#    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

