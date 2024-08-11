from pydantic import BaseModel
from typing import Optional
import time
from subprocess import Popen, PIPE, STDOUT
class msg_data_bytesExtra(BaseModel):
    userName: str
    nickName: str
    smallHeadImgUrl: str
    bigHeadImgUrl: str
    file: Optional[str]
    thumb: str
    image: str

class msg_data(BaseModel):
    sortIndex: int
    localId: int
    msgSvrID: str
    userName: str
    nickName: str
    smallHeadImgUrl: str
    bigHeadImgUrl: Optional[str]
    strContent: str
    msgSource: str
    createTime: int
    isSender: int
    type: int
    subType: int
    compressContent: Optional[str]
    bytesExtra: Optional[msg_data_bytesExtra]

async def msg_handler(data: msg_data):
    if data["userName"].find("@chatroom") != -1:
        data.append({"isChatroom": True})
    else:
        data.append({"isChatroom": False})




async def answer_old_
    daytime=time.strftime("%Y-%m-%d", time.localtime())
    #print(wxid,wxid_group,qu)
    qu=msg_data["strContent"]   #消息内容
    wxid=msg_data["userName"]  #消息发送人

    if data["isChatroom"]wxid_group=""
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



