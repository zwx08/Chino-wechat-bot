#默认为使用wxid作为userid，如果想要更改为使用单一userid请更改所有调用API_answer后的wxid改为userid
import action_sql
#from another_action import _a_ , image, name_write,data_name_write,read_name_all,warn,w_all
from another_action import *
from answerAPI import *
from more_action import *
import schedule
from sympy import *
from file_action import *
import sys,time
import xmltodict
from standard_print import *
config=config_read()
address=config["connect"]["sent_address"]
port=config["connect"]["sent_port"]
robotname=config["robotname"]
import plugins
import func_timeout



def run_plugin(row):
    global an_
    printinf(f"查询到qu_key({row['NAME']})")
    if row["an_way"] == "0":
        an_ = row["answer"]
    elif row["an_way"] == '1':
        #print(.411)
        Def=row["answer"]
        if Def.find("{plugin}") != -1:
            Def=Def.replace("{plugin}",f"plugins.{row['filename']}")
        try:
            an_=eval(f"{Def}")(l)
        except func_timeout.exceptions.FunctionTimedOut:
            printerr("qu_key({row['NAME']})执行超时")
            an_="超时-{row['NAME']}"
def keyword_(keyw,row):
    qu=l["qu"]
    if row["key_way"] == "0":
        #print(.21)
        if qu == keyw:
            #print(.31)
            return run_plugin(row)

    elif row["key_way"] == "1":
        #print(.22)
        #qu=qu.replace(":@ ","",1)
        if qu.find(keyw) == 0:
            #print(.32)
            return run_plugin(row)
    
    elif row["key_way"] == "2":
        #print(.23)
        if qu.find(keyw) != -1:
            #print(.33)
            return run_plugin(row)
def sql_row(rows):
    for row in rows:
        #print(row)
        if row["Enabled"] == 'True':
            keyword=ujson.loads(row["keyword"])
            #printinf(keyword)
            if isinstance(keyword,(list)) ==True:
                for key_x in keyword:
                    keyword_(key_x,row)
            if isinstance(keyword,(str,int)) ==True:
                keyword_(keyword,row)

def sql_row_access(rows):
    global an_
    for row in rows:
        if row["Enabled"] == 'True':
            if row["access_way"] == "0":
                Def=row["access"]
                if Def.find("{plugin}") != -1:
                    Def=Def.replace("{plugin}",f"plugins.{row['filename']}")
                try:
                    an_=eval(f"{Def}")(l)
                except func_timeout.exceptions.FunctionTimedOut:
                    printerr("access({row['NAME']})执行超时")
                #print(an_)



number_of_times={}   #每10s清空一次number_of_times
def clear_number_of_times():
    number_of_times.clear()
schedule.every(10).minutes.do(number_of_times.clear)

def run_an_replace(row,an):
    printinf(f"查询到an_replace{row['NAME']}")
    if row["re_way"] == "0":
        return an.replace(row["keyword"],row["replace"])
    elif row["re_way"] == '1':
        Def=row["replace"]
        if Def.find("{plugin}") != -1:
            Def=Def.replace("{plugin}",f"plugins.{row['filename']}")
        try:
            an=eval(f"{Def}")(l,an)
        except func_timeout.exceptions.FunctionTimedOut:
            printerr("qu_key({row['NAME']})执行超时")
            an="超时-an_replace({row['NAME']})"
    return an

def sql_row_an_replace(rows,an):
    for row in rows:
        if row["Enabled"] == 'True':
            if row["key_way"] == "0":
                if an == row["keyword"]:
                    an=run_an_replace(row,an)
            if row["key_way"] == "1":
                if an.find(row["keyword"]) != -1:
                    an=run_an_replace(row,an)
    return an
            
    
def send_msg_an():        #允许传入列表，实现每次调用加一次number_of_times[wxid_group]，且如果这个数字超过指定数量后不回复
    wxid=l["wxid"]
    wxid_group=l["wxid_group"]
    #print(an)
    if 'an_' != None :
        #print(an)

        #if 'wxid_group' in locals():
        #    if wxid_group in number_of_times:
        #        number_of_times[wxid_group] += 1
        #    else:
        #        number_of_times[wxid_group] = 1
        #    if number_of_times[wxid_group] > 5:
        #        return

        #else:
        if wxid in number_of_times:
                number_of_times[wxid] += 1
        else:
                number_of_times[wxid] = 1
        if number_of_times[wxid] > 10:
                return
        
        
        if an_=="":
            return
        
        
        if isinstance(an_,(str,int)) ==True:
            
            send_msg(wxid,sql_row_an_replace(action_sql.an_replace.read(),an_))
        elif isinstance(an_,(list)) ==True:
            for x in an_:
                send_msg(wxid,sql_row_an_replace(action_sql.an_replace.read(),x))
        else:
            send_msg(wxid,str(an_))
    return




@func_timeout.func_set_timeout(30)
def answer(wxid,wxid_group,qu):  #主调用
    data=data_read()
    global an_
    an_=None
    
    qu_xml=qu_xml_data=qu_reply_content=qu_reply_wxid=None
    if qu.find("<?xml") != -1:
        qu_xml=qu
        try:
            qu_xml_data=xmltodict.parse(qu)
        except:
            pass
        try:
            qu=qu_xml_data["msg"]['appmsg']['title']
            if "msg" in qu_xml_data:
                if 'appmsg' in qu_xml_data["msg"]:
                    if 'refermsg' in qu_xml_data["msg"]['appmsg']:
                        qu_reply_content=qu_xml_data["msg"]['appmsg']['refermsg']['content']
                        qu_reply_wxid=qu_xml_data["msg"]['appmsg']['refermsg']['chatusr']#如果是None是回复的消息与发送这条回复消息的人是一个人(注意由于提前已经定义为None，所以需要先行判断是否有qu_reply_content)
                #if 'img' in qu_xml_data["msg"]:
        except:
            pass
        
    if qu.find("@") == 0:
        if wxid_group != "":
            own_inf=data["own_inf"]
            own_inf_group=get_group_nickname(wxid,own_inf["wxid"])
            if own_inf_group['nickName'] != "":
                own_inf_group_nickname=own_inf_group['nickName']
            else:
                own_inf_group_nickname=own_inf["nickName"]
            #print(f"@{own_inf_group_nickname}")
            if qu.find(f"@{own_inf_group_nickname}") != -1:
                qu=qu.replace(f"@{own_inf_group_nickname}",":@")
            #print(qu)
        
        
    if wxid_group != None:
        if qu_xml_data != None:
            printmsg.rece(f"{wxid}({wxid_group}) >> {qu_xml_data}")
        else:
            printmsg.rece(f"{wxid}({wxid_group}) >> {qu}")
    else:
        if qu_xml_data != None:
            printmsg.rece(f"{wxid} >> {qu_xml_data}")
        else:
            printmsg.rece(f"{wxid} >> {qu}")
            
    
    global l
    l={"robotname":robotname,"qu":qu,"wxid":wxid,"wxid_group":wxid_group,"qu_xml":qu_xml,"qu_xml_data":qu_xml_data,"qu_reply_content":qu_reply_content,"qu_reply_wxid":qu_reply_wxid}

    
    #admin部分
    data=data_read()
    wxid_admin=data["wxid_admin"]
    if wxid in wxid_admin or wxid_group in wxid_admin:
        sql_row(action_sql.qu_key.admin.read())
        if an_ != None:
            send_msg_an()
            return
    
    #黑白名单，有bug（确信）   #黑白名单中除了wxid也可以写入 xxx@chatroom （理论上)   ，但是似乎写了chatroom应该是这个chatroom中的所有人都可以用，且要注意这个不能从比如说昵称啊什么的（wfc）转换成wxid，所以添加的时候请直接添加wxid等
    block=data["wxid_block"]
    white=data["wxid_white"]
    if (wxid or wxid_group)  in block:    #黑名单
        return
    if len(white) != 0: 
        if (wxid or wxid_group) not in white:   #白名单
            return

    #other部分
    sql_row(action_sql.qu_key.read())
    if an_ != None :
        send_msg_an()
        return
    #access接入部分
    sql_row_access(action_sql.access.read())
    #print(an_)
    if an_ != None :
        send_msg_an()
        return
    return

    #answerAPI部分
    answer=API_answer(qu,wxid)
    if 'status' in answer:
        st=answer['status']
    if 'answer' in answer :
        an_=answer['answer']
    if 'options' in answer:
            options=answer['options']
            an_=an_+ '  :  ' + str(options)

    if an_ != None :
        send_msg_an()
        return


if __name__ == "__main__":
    qu=""
    
    
    #print(sys.argv)
    for x in sys.argv[3:]:
        qu=f"{qu} {x}"
    qu=qu.strip()
    #print(sys.argv[1],sys.argv[2],qu)
    
    #print(qu)
    try:
        answer(sys.argv[1],sys.argv[2],qu)
    except func_timeout.exceptions.FunctionTimedOut:
        printerr("主函数执行超时")
        send_msg="timeout-主函数执行超时"
    




