import json
import os
from .file_action import data_read
from .api_action import get_bot_details
import ujson
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class OwnInf(BaseModel):
    userName: Optional[str] = None
    nickName: Optional[str] = None
    alias: Optional[str] = None
    mobile: Optional[str] = None
    sex: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    signature: Optional[str] = None
    bigHeadImgUrl: Optional[str] = None
    smallHeadImgUrl: Optional[str] = None

class wx_data_model(BaseModel):
    wxid_admin: List[str] = Field(default_factory=list)
    wxid_block: List[str] = Field(default_factory=list)
    wxid_white: List[str] = Field(default_factory=list)
    wx_name: Dict[str, str] = Field(default_factory=dict)
    wx_warn: Dict[str, dict] = Field(default_factory=dict)
    own_inf: OwnInf = Field(default_factory=OwnInf)
    ca_save: Dict = Field(default_factory=dict)


wx_data_file=os.path.join(os.path.dirname(__file__),"wx_data.json")
def preload():

    if not os.path.isfile(wx_data_file):
        # 文件不存在，创建文件
        with open(wx_data_file, 'w') as fp:
            fp.write(json.dumps({}))

    own_inf=get_bot_details()
    #own_inf_wxid=own_inf["data"]["wxid"]
    #own_inf_nickName=own_inf["data"]["nickName"]
    #own_inf_account=own_inf["data"]["account"]
    #own_inf_headerSmall=own_inf["data"]["headerSmall"]
    #owninf={"wxid":own_inf_wxid,"nickname":own_inf_nickName,"account":own_inf_account,"headerSmall":own_inf_headerSmall}
    try:
        data=wx_data_model(**data_read())
    except:
        data=wx_data_model()
    with open(os.path.join(wx_data_file), 'w', encoding='utf-8') as file:
        data.own_inf=OwnInf(**own_inf.data.model_dump())
        data_json=ujson.dumps(data.model_dump(), ensure_ascii=False, indent=4)
        file.write(data_json)
        file.close()

if __name__=="__main__":
    preload()