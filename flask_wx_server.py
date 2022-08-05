#!/usr/bin/python
# -*- coding: UTF-8 -*-
#此文件直接执行

import sys
import time
import ujson
import requests
from flask import Flask, request
from answer import answer
from file_action import *
import threading,subprocess

config=config_read()
address=config["connect"]["rece_address"]
port=config["connect"]["rece_port"]  #信息接收端口

        
#class myThread (threading.Thread):   # 继承父类threading.Thread
#    def __init__(self,wxid,qu,wxid_group,name):
#        threading.Thread.__init__(self)
#        self.threadName = name
#        self.wxid = wxid
#        self.qu = qu
#        self.wxid_group = wxid_group
        

#    def run(self):   # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#        answer(self.wxid,self.qu,self.wxid_group)

        

web = requests.session()
web.headers['Content-Type'] = 'application/x-www-form-urlencoded'

app = Flask(__name__)


@app.route('/', methods=['POST'])
def jieshou():
    strs = request.get_data()  # 字节流
    msg = ujson.loads(strs)  #此部分为消息接收端，这里将ujson转换为python字典
    #print(msg)            #调试用
    if msg['api'] == 1005:
        msg_data=msg["data"]    #1005消息主体
        qu=msg_data["StrContent"]   #消息内容
        wxid=msg_data["StrTalker"]  #消息发送人
        wxid_group=""
        if '@chatroom' in wxid :
            byte=msg_data["BytesExtra"]
            wxid_group =byte['wxid']
        if msg_data["IsSender"] == 0:     #判断是否是自己发的
            daytime=time.strftime("%%Y-%m-%d", time.localtime()) 
            with subprocess.Popen(["python","./answer.py",wxid,wxid_group,qu], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p, \
                open(f'./logs/wx_answer_{daytime}.log', 'ab') as file:
                for line in p.stdout: # b'\n'-separated lines
                    sys.stdout.buffer.write(line) # pass bytes as is
                    file.write(line)
            #with open("wx_answer_out.log","a") as out, open("wx_answer_err.log","a") as err:
            #    subprocess.Popen(["python","./answer.py",wxid,wxid_group,qu],  # 需要执行的文件路径
            #                        stdout = out,
            #                        stderr = err,
            #                        bufsize=1)
            return
    return ''


if __name__ == '__main__':
    app.run(host=address, port=port, debug=True, threaded=True)