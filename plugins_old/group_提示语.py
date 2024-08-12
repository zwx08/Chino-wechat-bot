import os
from action_sql import plugins_sql, qu_key


if __name__ =='__main__':
    #插件信息写入
    plugins_sql.inf("群管理-提示语",0.01,"zwx08","群管理-提示语")
    qu_key.write("群管理-提示语-&m","&m",0,"不准骂人！",0)
    qu_key.write("群管理-提示语-&a","&a",0,"不准聊天!",0)
    qu_key.write("群管理-提示语-&i","&i",0,"不要在这个群发无关图片啊喂！",0)
    qu_key.write("群管理-提示语-&h","&h",0,"涩涩，达咩",0)
    qu_key.write("群管理-提示语-&h1","&h1",0,"涩涩达咩!",0)
    qu_key.write("群管理-提示语-&ad","&ad",0,"广告达咩！",0)
    qu_key.write("群管理-提示语-&s","&s",0,"刷屏警告！",0)