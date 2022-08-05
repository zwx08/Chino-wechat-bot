from dataclasses import replace
from another_action_base import nickname
from more_action import get_group_nickname, get_own_infomation, get_wxid_details
qu="@智乃酱かふう ちの 123"
wxid="19055248888@chatroom"
own_inf=get_wxid_details()
own_inf_wxid=own_inf["data"]["wxid"]
own_inf_nickName=own_inf["data"]["nickName"]
own_inf_account=own_inf["data"]["account"]
own_inf_headerSmall=own_inf["data"]["headerSmall"]
owninf={"wxid":own_inf_wxid,"nickname":own_inf_nickName,"account":own_inf_account,"headerSmall":own_inf_headerSmall}
own_inf_group=get_group_nickname(wxid,owninf["wxid"])
if own_inf_group['nickName'] != "":
    own_inf_group_nickname=own_inf_group['nickName']
else:
    own_inf_group_nickname=own_inf_nickName
print(f"@{own_inf_group_nickname}")
if qu.find(f"@{own_inf_group_nickname}") != -1:
    qu=qu.replace(f"@{own_inf_group_nickname}",":@")
print(qu)