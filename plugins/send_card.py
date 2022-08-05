from action_sql import plugins_sql, qu_key
from more_action import invite_group, send_friend
from action_plugins import config

first_content="""chatroom: #群聊
# xxx@chatroom:
#  - xx

wxid_: #好友
# wxid_xxx:
#  - xxx

gh_: #公众号
# gh_xxx:
#  - xxxx"""

def send_card(qu,wxid):
    conf=config.read("send_card")
    #print(conf)
    for x,y in conf.items():
        if x=="chatroom":
            if y != None:
                for send,key in y.items():
                    for z in key:
                        if qu.find(z) != -1:
                            invite_group(send,wxid)
        elif x=="wxid_":
            if y != None:
                for send,key in y.items():
                    for z in key:
                        if qu.find(z) != -1:
                            send_friend(send,wxid,0)
        elif x=="gh_":
            if y != None:
                for send,key in y.items():
                    for z in key:
                        if qu.find(z) != -1:
                            send_friend(send,wxid,1)
                    
            
def main(l):
    qu=l["qu"]
    wxid=l["wxid"]
    send_card(qu,wxid)


if __name__ == "__main__":
    #插件信息写入
    plugins_sql.inf("send_card",0.01,"zwx08","发送群名片")
    qu_key.write("send_card","&send",1,"plugins.send_card.main",1,"发送群名片")
    config.first("send_card",first_content)
    