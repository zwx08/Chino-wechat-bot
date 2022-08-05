#此代码无法正常使用


import httpx,os
from io import BytesIO
from PIL import Image

from more_action import send_msg
from action_sql import plugins_sql, qu_key
def get(text):
    req=httpx.post("https://api.xingzhige.com/API/Qrcode/",data={"text":text})
    print(req.content)
    image=Image.open(BytesIO(req.content))
    fileName="qrcode_cache"+'.'+image.format.lower()
    cache=os.path.join(os.getcwd(),"cache",fileName)
    with open(cache,'wb') as f:
        f.write(req.content)
    return cache

def main(l):
    text=l["qu"][8:]
    wxid=l["wxid"]
    cache=get(text)
    send_msg(wxid,cache,3)
    
if __name__=="__main__":
    plugins_sql.inf("qrcode",0.01,"zwx08","生成qrcode")
    qu_key.write("qrcode","&qrcode",1,"{plugin}.main",1)