from action_sql import plugins_sql, qu_key
from another_action_base import wxid_form_cr
from more_action import delete_group_members

def  del_group(l):
    qu=l["qu"]
    wxid=l["wxid"]
    qu_data=qu.splitlines()
    sender=qu_data[1]
    if qu_data[1][:3] != "wxid":
        wxi=wxid_form_cr(wxid,sender)
        if wxi==None:
            return "error_wfc"
    elif qu_data[1][:3] == "wxid":
        wxi=sender
    delete_group_members(wxid,wxi)
    return "success"
if __name__ =='__main__':
    #插件信息写入
    plugins_sql.inf("群管理-基础",0.01,"zwx08","群管理-基础")
    qu_key.admin.write("群管理-基础-删除群成员","&del_group",1,'{plugin}.del_group',1)