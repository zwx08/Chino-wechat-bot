#此文件直接执行
#本例子只开启http端口接收，使用post方法
#此文件需answer.py

import ujson,json
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
from _action import *
from answer import *
from another_action import *
from file_action import *
import threading,subprocess,sys,os
import os,sys
from subprocess import Popen, PIPE, STDOUT
def ans_popen(wxid,wxid_group,qu):
    current_encoding = 'utf-8'
    popen = subprocess.Popen(["python","./answer.py",wxid,wxid_group,qu],  # 需要执行的文件路径
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            bufsize=1)
    # 重定向标准输出
    while popen.poll() is None:                      # None表示正在执行中
        r = popen.stdout.readline().decode(current_encoding)
        sys.stdout.write(r)                                # 可修改输出方式，比如控制台、文件等
        
    # 重定向错误输出
    if popen.poll() != 0:                      # 不为0表示执行错误
        err = popen.stderr.read().decode(current_encoding)
        sys.stdout.write(err)                 # 可修改输出方式，比如控制台、文件等   
        


config=config_read()
address=config["connect"]["rece_address"]
port=config["connect"]["rece_port"]  #信息接收端口
class myThread (threading.Thread):   # 继承父类threading.Thread
    def __init__(self,wxid,qu,wxid_group):
        threading.Thread.__init__(self)
        self.wxid = wxid
        self.qu = qu
        self.wxid_group = wxid_group
    def run(self):   # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        answer(self.wxid,self.wxid_group,self.qu)

class MyHTTPServer(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['content-length']))  # 接收参数
        strs = str(data , encoding='utf-8')
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
                daytime=time.strftime("%Y-%m-%d", time.localtime()) 
                #print(wxid,wxid_group,qu)
                with Popen(["python","./answer.py",wxid,wxid_group,qu], stdout=PIPE, stderr=STDOUT) as p, \
                    open(f'./logs/wx_answer_{daytime}.log', 'ab+') as file:
                    for line in p.stdout: # b'\n'-separated lines
                        sys.stdout.buffer.write(line) # pass bytes as is
                        file.write(line)
                #with open("wx_answer_out.log","a") as out, open("wx_answer_err.log","a") as err:
                #    subprocess.Popen(["python","./answer.py",wxid,wxid_group,qu],  # 需要执行的文件路径
                #                        stdout = out,
                #                        stderr = err,
                #                        bufsize=1)
                return

class server:
    def httpserver(self):
        server = HTTPServer((address , port) , MyHTTPServer)
        print(f"{server.server_address}servers启动成功")
        server.handle_request()
        server.serve_forever()

if __name__ == '__main__':
    a=server()
    a.httpserver()
