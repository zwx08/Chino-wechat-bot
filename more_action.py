import time
from httplib2 import Response
import requests as httpx
from file_action import *
import ujson,json,xmltodict

from standard_print import printerr, printmsg, printres

config=config_read()
address=config["connect"]["sent_address"]
port=config["connect"]["sent_port"]


def Request(way,api,data=None,param1=None,param2=None,param3=None):
    if param1 == None:
        apiurl=f"http://{address}:{port}/?api={api}"
    elif param2 == None:
        apiurl=f"http://{address}:{port}/?api={api}&param={param1}"
    elif param3 == None:
        apiurl=f"http://{address}:{port}/?api={api}&param1={param1}&param2={param2}"
    else:
        apiurl=f"http://{address}:{port}/?api={api}&param1={param1}&param2={param2}&param3={param3}"
    if way == "get":
        res_json = httpx.get(apiurl).text
    if way == "post":
        if data == None:
            res_json = httpx.post(apiurl)
        else:
            res_json = httpx.post(apiurl , json=data)
    try:
        res=ujson.loads(res_json)
    except:
        res=res_json
    printres(res)
    return res

#以下内容皆未测试

#消息功能
#https://www.showdoc.com.cn/wx2api/8905085800157296
#type：消息类型：1 文本消息 ，2 文件消息， 3 图片消息， 4 GIF动画表情消息
def send_msg(wxid,content,type=1,isUnicodeEscape=1):

    if content.find("<?xml") != -1:
        try:
            content_xml=xmltodict.parse(content)
        except:
            pass
    printmsg.send(f"{wxid} << {content}")
    return Request("post",8,{"api":8,"isUnicodeEscape":isUnicodeEscape,"content":content,"type":type,"wxid":wxid})
    
#https://www.showdoc.com.cn/wx2api/8905086274002428
def send_xml(wxid,content):
    return Request("post",101,{"api": 101,"recverWxid": wxid,"content":content})
    
#https://www.showdoc.com.cn/wx2api/8905087650547309
def send_art(des,wxid,thumbUrl,title,url):
    return Request("post",10,{"api": 10,"des": des, "recverWxid": wxid,"thumbUrl": thumbUrl,"title": title,"url": url})

#https://www.showdoc.com.cn/wx2api/8905149941770554 
#type：ype: 1 文本 ， 3 图片XML ，47 动态表情XML ， 49 文件 链接 小程序XML
def send_quo(content,type,wxid,param):
    return Request("post",96,{"api":96,"content":content,"type":type,"wxid":wxid,"param":param})

#https://www.showdoc.com.cn/wx2api/8905088612820763
def send_forward(wxid,id=None,MsgSvrID=None):
    if id != None:
        return Request("get",10086,param1=wxid,param2=id)
    if MsgSvrID != None:
        return Request("get",10087,param1=wxid,param2=MsgSvrID)

#https://www.showdoc.com.cn/wx2api/8905150796768180
def send_recall(wxid,serverId=None,localId=None):
    if serverId != None:
        return Request("get",10010,param1=wxid,param2=serverId)
    if localId != None:
        return Request("get",10011,param1=wxid,param2=localId)

#https://www.showdoc.com.cn/wx2api/8905151169084513
def get_original_picture(xml,image,thumb=None):
    if thumb == None:
        return Request("post",1033,{"api":1033,"xml":xml,"image":image})
    else:
        return Request("post",1033,{"api":1033,"xml":xml,"image":image,"thumb":thumb})

#收藏消息





#通讯录功能
#https://www.showdoc.com.cn/wx2api/8905090079162044
def get_wxid_details(wxid=None):
    if wxid == None:
        return Request("get",4)
    else:
        return Request("get",4,param1=wxid)



#https://www.showdoc.com.cn/wx2api/8905101261842176
def auto_add_friends(param1=1):
    return Request("get",75,param1=param1)

#https://www.showdoc.com.cn/wx2api/8905089136175178
def send_friend(wxid_send,wxid,type=0):
    return Request("post",16,data={"api":16,"param1":wxid_send,"param2":wxid,"type":type})


#群组功能
#https://www.showdoc.com.cn/wx2api/8905102904669735
def invite_group(wxid_send,wxid):
    if isinstance(wxid,list) == True:
        return Request("post",210,{"api":210, "param1":wxid_send, "param2":wxid})
    if isinstance(wxid,str) == True:
        return Request("post",21,{"api":21, "param1":wxid_send, "param2":wxid})
    else:
        printerr("Error for unsupported form(invite_group)") 


#https://www.showdoc.com.cn/wx2api/8905128344265365
def get_group_nickname(wxid,wxid_group_get=None):
    return Request("get",806,param1=wxid,param2=wxid_group_get)


def delete_group_members(wxid,wxid_group):
    return Request("post",25,data={"api":25,"param1":wxid,"param2":wxid_group})



#登录
#https://www.showdoc.com.cn/wx2api/8905084291904840
def check_wxchat_logging():
    return Request("get",1)

#https://www.showdoc.com.cn/wx2api/8905083174377643
def get_QR_code_URL():
    return Request("get",2)

#https://www.showdoc.com.cn/wx2api/8905083816268892
def get_QR_code():
    return Request("get",3)

#https://www.showdoc.com.cn/wx2api/8905082409027795
def open_another_and_injection(port_another):
    return Request("get",31,param1=port_another)

















def get_original_picture(port,wxid,xml,image):   #测试未成功，不要用
    apiurl=f"http://{address}:{port}"
    data={"api": 1033,"xml":xml,"image":image}
    res = httpx.post(apiurl , json=data)
    print(res.text)


def get_original_picture_2(port,wxid,xml,image):  #测试未成功，不要用
    apiurl=f"http://{address}:{port}"
    data={"api": 1033,"xml":xml,"image":image}
    res = httpx.post(apiurl , json=data)
    print(res.text)

def update_group_member_details(wxid,wxid_group):
    return Request("get",805,None,wxid,wxid_group)

def get_chatroom_details_all(chatroom):
    return Request("get",552,None,chatroom)
