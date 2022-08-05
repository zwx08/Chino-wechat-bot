from action_sql import an_replace, plugins_sql, qu_key
from another_action_base import wxid_form_cr
from file_action import data_read
from more_action import get_wxid_details
import ujson

class call: #称呼
    
    def data_name_write(name_write,name_write_call):
        data=data_read()
        with open('wx_data.json', 'w', encoding='utf-8') as file:
            data["wx_name"][name_write]=name_write_call
            data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
            file.write(data_json)
            file.close()

    def _a_ (l,an):
        wxid=l["wxid"]
        wxid_group=l["wxid_group"]
        
        if an.find('_a_') != -1 :
            data=data_read()
            wx_name=data["wx_name"]
            if wxid_group:
                wxid=wxid_group

                #    print(wx_name[wxid])
                if wxid in wx_name:
                    anr=an.replace('_a_',wx_name[wxid])

                #        print("有",anr)
                else:
                    #update_group_member_details(port,wxid,wxid_group)
                    wxid_de=get_wxid_details(wxid_group)
                    nickname=(wxid_de["data"])["nickname"]
                    #print(nickname)
                    anr=an.replace('_a_',nickname)
                #        print('无')
                return anr
        else:
            return an

    def name_write(l):
        wxid=l["wxid"]
        qu=l["qu"]
        qu_data=qu.splitlines()
        #get_chatroom_details_all(wxid)
        if qu_data[1][:3] == "wxid":
           wxid=qu_data[1] 
        else:
            wxid=wxid_form_cr(wxid,qu_data[1])
        if wxid==None:
            return "error"
        call.data_name_write(wxid,qu_data[2])


    def read_name_all(l):
        data=data_read()
        data_json=ujson.dumps(data["wx_name"], ensure_ascii=False, indent=4)
        return data_json
    

if __name__ =="__main__":
    plugins_sql.inf("call",0.01,"zwx08","称呼")
    qu_key.admin.write("call","&call",1,'{plugin}.call.name_write',1,"称呼写入")
    qu_key.write("read_name_all","&c_all",0,"{plugin}.call.read_name_all",1,"所有称呼读取")
    an_replace.write("call","_a_",1,"{plugin}.call._a_",1,"称呼替换")