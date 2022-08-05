#自设字符转换:此例子使用_a_作为字符转换，an例子:_a_好~
#随机图片注意:文件夹中文件格式必须为微信支持图片格式,且不得有乱码文件，部分在action.py中有写，如果有其他微信支持扩展名（比如jpeg)，请按照action中格式添加到action.py

from more_action import *
from file_action import *
from another_action_base import *
import httpx,ujson
from sympy import *

class call: #称呼
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
                    wxid_de=get_wxid_details(wxid_group)
                    nickname=(wxid_de["data"])["nickname"]
                    #print(nickname)
                    anr=an.replace('_a_',nickname)
                #        print('无')
                return anr
        else:
            return an

    def name_write(qu,wxid):
        qu_data=qu.splitlines()
        #get_chatroom_details_all(wxid)
        if qu_data[1][:3] == "wxid":
           wxid=qu_data[1] 
        else:
            wxid=wxid_form_cr(wxid,qu_data[1])
        if wxid==None:
            return "error"
        call.data_name_write(wxid,qu_data[2])


    def read_name_all():
        data=data_read()
        data_json=ujson.dumps(data["wx_name"], ensure_ascii=False, indent=4)
        return data_json


class warn: #警告
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



    def warn(qu,wxid):
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
            return f"警告:{nickname(wxi)}-{wxi}({wxid}:{time}/16)\n原因:{qu_data[2]}"
        else:
            return f"警告:{nickname(wxi)}-{wxi}({wxid}:{time}/16)"

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
        
class another_data_write: #其他data.json的写入
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
    


    


def image(wxid): #随机图片
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
    send_msg(wxid,image,3)
    return ""
