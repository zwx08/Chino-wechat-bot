import httpx
from file_action import *

config=config_read()
address=config["connect"]["sent_address"]
port=config["connect"]["sent_port"]

#发送消息
def sent_msg(port,wxid,content):
    apiurl=f"http://{address}:{port}"

    if str(".jpg") in content or str(".png") in content or str(".gif") in content or str("jpeg") in content:
        #发送图片的json
        #content为图片的本地地址
        data = {"api": 8 , "content": content , "type": 3 , "wxid": wxid}
    else:
        #发送文本的json
        #wxid分为个人、群wxid,
        data = {"api": 8 , "content": content , "type": 1 , "wxid": wxid}
    res = httpx.post(apiurl , json=data)
    try:
        res=ujson.load(res)
    except:
        res=res
    print(res)
    return res
    

#获取好友详细信息
def get_userinfo(port,wxid):
    if len(wxid) != 0:
        #wxid非空，获取好友的信息
        apiurl=f"http://{address}:{port}/?api=4&param={wxid}"
    else:
        # wxid为空，获取自己的信息
        apiurl = f"http://{address}:{port}/?api=4"
    data={"api": 4}
    res=httpx.get(apiurl , json=data)
    return res

def get_msg(msg):#消息来自哪里,消息类型为msg['type']==1005
    if '@chatroom' in msg['data']['StrTalker']:#群文本消息
        print("群消息")
        data={}
    if len(msg['data']['BytesExtra']) == 0:
        print("私聊消息")
        data={}
    return data

