from action_sql import an_replace, plugins_sql, qu_key
from file_action import config_read
from more_action import get_wxid_details, send_msg, update_group_member_details
import yaml


def ugmd(l):
    qu=l["qu"]
    wxid=l["wxid"]
    qu_data=qu.splitlines()
    for x in qu_data[1:]:
        print(x)
        update_group_member_details(wxid,x)
        
    return "s"
def userinfo(l):
    qu=l["qu"]
    wxid=l["wxid"]
    userinfo_wxid=qu.splitlines()
    for x in userinfo_wxid[1:]:
        print(x)
        content=yaml.dump(get_wxid_details(x)["data"], sort_keys=False, default_flow_style=False,encoding='utf-8',allow_unicode=True)
        send_msg(wxid,content.decode('UTF-8'))
        
    
if __name__=="__main__":
    plugins_sql.inf("robot_base",0.01,"zwx08","robot_基础")
    qu_key.write("ugmd","&ugmd",1,'{plugin}.ugmd',1,"更新群成员详细信息")
    qu_key.write("userinfo","&userinfo",1,'{plugin}.userinfo',1,"获取群成员详细信息")
    config=config_read()
    robotname=config["robotname"]
    an_replace.write("robotname","_robotname_",1,robotname,0,"_robotname_的替换")