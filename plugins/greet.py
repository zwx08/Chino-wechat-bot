#此代码无法正常使用

import time

from action_sql import plugins_sql, qu_key
from file_action import config_read

def main(l):
    an=None
    qu=l["qu"]
    struct_times = time.localtime(time.time())
    morning=(struct_times.tm_hour) >= 0 and (struct_times.tm_hour) < 12
    afternoon=(struct_times.tm_hour) >= 12 and (struct_times.tm_hour) < 18
    noon=(struct_times.tm_hour) >= 11 and (struct_times.tm_hour) <= 14
    night=(struct_times.tm_hour) >= 16 and (struct_times.tm_hour) < 24
    night_morn=(struct_times.tm_hour) >= 0 and (struct_times.tm_hour) < 6
    if morning:
        ti="早上"
    if afternoon:
        ti="下午"
    if night:
        ti="晚上"
    if night_morn:
        ti="凌晨"
    if noon:
        ti="中午"



    if qu.find("晚安") != -1:
        an="_a_晚安~"
    if qu.find("早安") != -1:
        an="_a_早安~"
    if qu.find("午安") != -1:
        an="_a_午安~"


    if qu.find("好") != -1:
        
        if qu.find("上午") != -1:
            if morning:
                an="_a_上午好~"
            else:
                an="啊喂！都"+ti+"了呢~"
        if qu.find("早上") != -1:
            if morning:
                an="_a_早上好~"
            elif afternoon:
                an="啊喂！都下午了呢~"
            else:
                an="啊喂！都"+ti+"了呢~"
        if qu.find("下午") != -1:
            if afternoon:
                an="_a_下午好~"
            else:
                an="啊喂！都"+ti+"了呢~"
        if qu.find("中午") != -1:
            if noon:
                an="_a_中午好~"
            else:
                an="啊喂！都"+ti+"了呢~"
        if qu.find("晚上") != -1:
            if night:
                an="_a_晚上好~"
            elif night_morn:
                an="都早上了吧~"
            else:
                an="啊喂！都"+ti+"了呢~"

    if (qu.find("早呀") != -1 and qu.find("各位") != -1) or qu.find("大家早") != -1:
        an="_a_早~"

    if "an" != None:
        return an
if __name__ =="__main__":
    config=config_read()
    robotname=config["robotname"]
    plugins_sql.inf("greet",0.01,"zwx08","问候")
    qu_key.write("greet",[":@",robotname],1,"{plugin}.main",1,"greet_早/中/晚好",Enabled=False)