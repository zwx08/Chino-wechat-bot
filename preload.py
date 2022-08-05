import json
import os
from file_action import data_read, data_write
from more_action import get_wxid_details
import ujson

own_inf=get_wxid_details()
#own_inf_wxid=own_inf["data"]["wxid"]
#own_inf_nickName=own_inf["data"]["nickName"]
#own_inf_account=own_inf["data"]["account"]
#own_inf_headerSmall=own_inf["data"]["headerSmall"]
#owninf={"wxid":own_inf_wxid,"nickname":own_inf_nickName,"account":own_inf_account,"headerSmall":own_inf_headerSmall}
data=data_read()
with open('wx_data.json', 'w', encoding='utf-8') as file:
    try:
        data["own_inf"].update(own_inf["data"])
    except:
        data["own_inf"]={} 
        data["own_inf"].update(own_inf["data"])
    data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
    file.write(data_json)
    file.close()

