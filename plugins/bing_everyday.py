import httpx,os
from io import BytesIO
from PIL import Image

from more_action import send_msg
from action_sql import plugins_sql, qu_key

def get():
    req=httpx.get("https://api.xingzhige.com/API/Bing_img/")
    image=Image.open(BytesIO(req.content))
    fileName="bing_everyday_cache"+'.'+image.format.lower()
    cache=os.path.join(os.getcwd(),"cache",fileName)
    with open(cache,'wb') as f:
        f.write(req.content)
    return cache
def main(l):
    wxid=l["wxid"]
    cache=get()
    send_msg(wxid,cache,2)
    
if __name__=="__main__":
    plugins_sql.inf("bing_everyday",0.01,"zwx08","bing每日美图")
    qu_key.write("bing_everyday","&bing",0,"{plugin}.main",1)