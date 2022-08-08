#版本号 1.0.0.2
#此文件接入微信对话开放平台https://openai.weixin.qq.com/，此处使用接口文档https://developers.weixin.qq.com/doc/aispeech/confapi/INTERFACEDOCUMENT.html

import httpx
import json,ujson
from _action import *
from action_sql import access
from file_action import *
import time
import urllib3

from standard_print import printerr, printinf
urllib3.disable_warnings()

config=config_read()
TOKEN=config["answerAPI"]["TOKEN"]
managerid=config["answerAPI"]["managerid"]


#API_signature

def API_signature(userid):
    printinf('请求signture')
    sign_url = 'https://openai.weixin.qq.com/openapi/sign/'+TOKEN
    sign_data = {'userid': userid}
    global signature
    signature_json = httpx.post(sign_url,  data = sign_data)
    signature = signature_json.json()
    #sign[userid]=signature['signature']
    with open('sign.json', 'r', encoding='utf-8') as file:
        sign_json = file.read()
        sign=ujson.loads(sign_json)
        
        sign[userid]=signature['signature']
        
    with open('sign.json', 'w', encoding='utf-8') as file:
        sign_json=ujson.dumps(sign, ensure_ascii=False, indent=4)
        file.write(sign_json)
        

    

def API_an(userid,qu):
    with open('sign.json', 'r', encoding='utf-8') as file:
        sign_json = file.read()
        sign=ujson.loads(sign_json)
    url = 'https://openai.weixin.qq.com/openapi/aibot/'+TOKEN
    an_data = {'signature': sign[userid] , 'query': qu }
    answer_json = httpx.post(url, data = an_data)
    answer = answer_json.json()
    
    if "errcode" in answer or "errmsg" in answer:
        if "errcode" in answer and "errmsg" in answer:
            printerr('错误:'+answer['errmsg']+" ("+str(answer['errcode'])+")")
        elif "errcode" in answer:
            printerr('错误:'+str(answer['errcode']))
        elif "errmsg" in answer:
            printerr('错误:'+answer['errmsg'])
        errcode={1004 , 1005 , 1006}
        if answer['errcode'] in errcode:
            API_signature(userid)
            an_data = {'signature': sign[userid] , 'query': qu }
            answer_json = httpx.post(url, data = an_data)
            answer = answer_json.json()
    return answer


#API_answer
def API_answer(qu,userid):
    with open('sign.json', 'r', encoding='utf-8') as file:
        sign_json = file.read()
        sign=ujson.loads(sign_json)

    if userid in sign:
        answer = API_an(userid,qu)
    else:
        API_signature(userid)
        answer = API_an(userid,qu)
    return answer


def API_release():
    url='https://openai.weixin.qq.com/openapi/publish/'+TOKEN

    answer_json = httpx.post(url, data = 'data')
    answer = answer_json.json()
    if answer['errcode']:
        return answer['errcode']



def API_Import(qu):
    url='https://openai.weixin.qq.com/openapi/batchimportskill/'+TOKEN
    
    data={
        'managerid': managerid , 
        'skill':qu.replace('^m ',"")
        }
    answer_json = httpx.post(url, data = data)
    answer = answer_json.json()
    printerr(answer["errcode"])
    return(answer["errcode"])


def main(l):
    an = None
    qu=l["qu"]
    wxid=l["wxid"]
    answer=API_answer(qu,wxid)
    if 'status' in answer:
        st=answer['status']
    if 'answer' in answer :
        an=answer['answer']
    if 'options' in answer:
            options=answer['options']
            an=an+ '  :  ' + str(options)
    if an != None:
        return an

if __name__=="__main__":
    access.write("openai","{plugin}.main",0,"微信开放平台调用")
            
