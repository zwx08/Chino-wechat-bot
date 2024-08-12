from Chino_old.api_action import get_wxid_details,get_chatroom_details,get_chatroom_member
from .standard_print import printerr


def nickname(wxid_group):
    #update_group_member_details(port,wxid,wxid_group)
    wxid_de=get_wxid_details(wxid_group)
    nickname=wxid_de.data.nickName
    return nickname

def get_roomNick_in_chatroom(chatroom,userName):
    apiget=get_chatroom_member(chatroom)
    for member in apiget.data.member:
        # 检查当前成员的userName是否为我们要查找的userName
        if member.userName == userName:
            # 找到匹配项，返回其nickName
            if member.roomNick != '':
                return member.roomNick
            else:
                return member.nickName
    # 没有找到匹配的userName，返回None
    return None