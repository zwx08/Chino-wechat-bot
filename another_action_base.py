from more_action import *
from file_action import *
from standard_print import printerr


def nickname(wxid_group):
    #update_group_member_details(port,wxid,wxid_group)
    wxid_de=get_wxid_details(wxid_group)
    nickname=wxid_de["data"]["nickName"]
    return nickname
def wxid_form_cr(wxid,sender):
    if "@chatroom" in wxid:
        cda=get_chatroom_details_all(wxid)
        for x in cda['data']:
            if x["NickName"] == sender or x["Alias"] == sender or x["RoomNick"] == sender:
                return x["UserName"]
    else:
        printerr("Error for wxid is must be chatroom(wxid_form_cr)")
        return
    
