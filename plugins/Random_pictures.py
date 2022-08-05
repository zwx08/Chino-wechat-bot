from action_sql import plugins_sql, qu_key
from more_action import send_msg

rootdir=""  #更改为你自己放图片的文件夹
def image(wxid): #随机图片
    import os
    import random

    file_names = []
    for parent, dirnames, filenames in os.walk(rootdir):    #三个参数:分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        file_names = filenames
        # for filename in filenames:                        #输出文件信息
        #     print("parent is" + parent)
        #     print("filename is:" + filename)
        #     print("the full name of the file is:" + os.path.join(parent, filename))
    x = random.randint(0, len(file_names)-1)
    image=rootdir+"\\"+file_names[x]  
    send_msg(wxid,image,3)
    return ""



if __name__=="__main__":
    name="_robotname_"
    keyword=[name+"随便来个二次元吧",name+"来个图","来个二次元小姐姐",name+"随便来个二次元",name+"来张图"]
    plugins_sql.inf("Random_pictures",0.01,"zwx08","随机图片-本地")
    qu_key.write("Random_pictures",keyword,0,"{plugin}.image",1)