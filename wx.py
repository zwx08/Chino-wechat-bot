#http_server
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

port=12345#信息接收端口

class MyHTTPServer(BaseHTTPRequestHandler):
    def do_POST(self):
        global msg
        data = self.rfile.read(int(self.headers['content-length']))  # 接收参数
        strs = str(data , encoding='utf-8')
        msg = json.loads(strs)
        print(msg,type(msg))

class server:
    def httpserver(self):
        server = HTTPServer(('127.0.0.1' , port) , MyHTTPServer)
        print(f"{server.server_address}servers启动成功")

        server.handle_request()
        server.serve_forever()

if __name__ == '__main__':
    a=server()
    a.httpserver()

import requests
import json

qu = msg["StrContent"]
TOKEN='jlVtyafwsAdgfdiGMtBFqFzyKaWNU9'
sign_url = 'https://openai.weixin.qq.com/openapi/sign/'+TOKEN
sign_data = {'userid': 'zhinai'}

signature_json = requests.post(sign_url,  data = sign_data)
signature = signature_json.json()
print(signature)

url = 'https://openai.weixin.qq.com/openapi/aibot/'+TOKEN
an_data = {'signature': signature['signature'] , 'query': qu }
answer_json = requests.post(url, data = an_data)
answer = answer_json.json()

print (answer)
