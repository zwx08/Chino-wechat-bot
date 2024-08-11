from fastapi import FastAPI
from pydantic import BaseModel
from file_action import config_read
from msg_handler import msg_handler

config=config_read()
address=config["connect"]["rece_address"]
port=config["connect"]["rece_port"]  #信息接收端口


class Item(BaseModel):
    api: int
    wechat: str
    port: int
    pid: int
    msg: str
    errorCode: int
    errorMsg: str
    data: dict[str,str]



app = FastAPI()


@app.get("/")
async def root(item: Item):
    match  item.api():
        case 1005:
            msg_data=item.data()
            if msg_data["isSender"]!=1:
                msg_handler(msg_data)
            return
    return