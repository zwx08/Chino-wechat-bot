import os

import yaml
from action_sql import plugins_sql, qu_key
from another_action_base import nickname, wxid_form_cr
from file_action import data_read, data_write_data
import ujson

import plugins

class warn: #警告
    def data_warn_write(wxid,sender,t):
        data=data_read()
        if wxid in data["wx_warn"]:
            if sender in data["wx_warn"][wxid]:
                data["wx_warn"][wxid][sender] += t
            else:
                data["wx_warn"][wxid][sender] = t
        else:
            data["wx_warn"][wxid] = {}
            data["wx_warn"][wxid][sender] = t
        with open('wx_data.json', 'w', encoding='utf-8') as file:
            data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
            file.write(data_json)
            file.close()
        return data["wx_warn"][wxid][sender]



    def warn(l):
        qu=l["qu"]
        wxid=l["wxid"]
        qu_data=qu.splitlines()
        if len(qu_data[0]) > 6:
            t=qu_data[0][6:]
        else:
            t=1
        sender=qu_data[1]
        if qu_data[1][:5] != "wxid_":
            wxi=wxid_form_cr(wxid,sender)
            if wxi==None:
                return "error_wfc"
            
        elif qu_data[1][:5] == "wxid_":
            wxi=sender
        time=warn.data_warn_write(wxid,wxi,int(t))
        #name=_a_ ("_a_",qu_data[1],qu_data[1],port)
        try:
            nick=nickname(wxi)
        except:
            nick=wxi
        if 	len(qu_data) == 3:
            return f"警告:{nick}-{wxi}({wxid}:{time}/16)\n原因:{qu_data[2]}"
        else:
            return f"警告:{nick}-{wxi}({wxid}:{time}/16)"

    def w_all(l):
        wxid=l["wxid"]
        data=data_read()
        try:
            data_json=yaml.dump(data["wx_warn"][wxid], sort_keys=False, default_flow_style=False,allow_unicode=True)
        except KeyError:
            data_json=None
        return data_json
    def w_all_all():
        data=data_read()
        data_json=yaml.dump(data["wx_warn"], sort_keys=False, default_flow_style=False,allow_unicode=True)
        #data_json=ujson.dumps(data["wx_warn"], ensure_ascii=False, indent=4)
        return data_json
    def w_del(l):
        qu=l["qu"]
        wxid=l["wxid"]
        qu_data=qu.splitlines()
        if len(qu[0]) >7:
            wxid=qu[0][7:]
        for x in qu_data[1:]:
            if x[:3] != "wxid":
                wxi=wxid_form_cr(wxid,x)
                if wxi==None:
                    return "error_wfc"
        data=data_read()
        del data["wx_warn"][wxid][wxi]
        data_write_data(data)
        data=data_read()
        if wxi not in data["wx_warn"][wxid]:
            return "success"
        else:
            return "error"
        
if __name__ =="__main__":
    filename=os.path.basename(__file__)
    plugins_sql.inf(os.path.basename(__file__),"0.0.1","zwx08","群管理-警告")
    qu_key.admin.write("[group]warn","&warn",1,"{plugin}.warn.warn",1)
    qu_key.write("[group]warn","&w_all",1,"{plugin}.warn.w_all",1)
    qu_key.admin.write("[group]warn","&w_alll",1,"{plugin}.warn.w_all_all",1)
    qu_key.admin.write("[group]warn","&w_del",1,"{plugin}.warn.w_del",1)
    
