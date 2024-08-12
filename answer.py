#默认为使用wxid作为userid，如果想要更改为使用单一userid请更改所有调用API_answer后的wxid改为userid
from ast import Tuple
import os
from pluginlib import PluginLoader
import pluginlib

from Chino_old.model_definition import AnswerBase, AnswerBaseList
#from another_action import _a_ , image, name_write,data_name_write,read_name_all,warn,w_all
from  . import api_action as api
from .another_action_base import get_roomNick_in_chatroom
import schedule
# from sympy import *
from file_action import config_read
from .file_action import data_read
from .preload import preload
import sys
import xmltodict
from .standard_print import printerr,printinf,printmsg
from .standard_print import logger
import func_timeout
import ujson
import xml.etree.ElementTree as ET





config=config_read()
address=config.connect.host
port=config.connect.port
robotname=config.robotname
preload()
# load_plugins()

# row_qukey_admin=action_sql.qu_key.admin.read()
# row_qukey=action_sql.qu_key.read()
# row_access=action_sql.access.read()


loader = PluginLoader(paths=[os.path.join(os.path.dirname(__file__),"plugins")],group="msg_plugin")
plugins = loader.plugins
print("plugins"+str(  plugins))


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
            an_=eval(f"{Def}")(msg_l)
        except func_timeout.exceptions.FunctionTimedOut:
            printerr("qu_key({row['NAME']})执行超时")
            an_="超时-{row['NAME']}"
def keyword_(keyw,row):
    qu=msg_l["qu"]
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
        if row["Enabled"] == "True":

            keyword=ujson.loads(row["keyword"])
            #printinf(keyword)
            if isinstance(keyword,(list)) is True:
                for key_x in keyword:
                    keyword_(key_x,row)
            elif isinstance(keyword,(str,int)) is True:
                keyword_(keyword,row)

def sql_row_access(rows):
    global an_
    for row in rows:
        if row["Enabled"] == "True":
            if row["access_way"] == "0":
                Def=row["access"]
                if Def.find("{plugin}") != -1:
                    Def=Def.replace("{plugin}",f"plugins.{row['filename']}")
                try:
                    an_=eval(f"{Def}")(msg_l)
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
            an=eval(f"{Def}")(msg_l,an)
        except func_timeout.exceptions.FunctionTimedOut:
            printerr("qu_key({row['NAME']})执行超时")
            an="超时-an_replace({row['NAME']})"
    return an

def sql_row_an_replace(rows,an):
    for row in rows:
        if row["Enabled"] == "True":
            if row["key_way"] == "0":
                if an == row["keyword"]:
                    an=run_an_replace(row,an)
            elif row["key_way"] == "1":
                if an.find(row["keyword"]) != -1:
                    an=run_an_replace(row,an)
    return an



def Replace_msg(context:str):  #TODO
    ...


async def send_msg_an(plugin_result: AnswerBase):        #允许传入列表，实现每次调用加一次number_of_times[wxid_group]，且如果这个数字超过指定数量后不回复
    wxid=msg_l["wxid"]
    #wxid_group=l["wxid_group"]
    #print(an)

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
    answer_send=plugin_result.answer

    if isinstance(answer_send,str):
        if answer_send=="":
            logger.info("answer_send为空字符串")
            return

    if plugin_result.Replace:  #TODO
        pass






    match plugin_result.send_way:
        case "Text":
            if isinstance(answer_send,str):
                api.send_msg.text(wxid,answer_send)
            elif isinstance(answer_send,dict):
                api.send_msg.text(wxid,**answer_send)
        case "Image":
            if isinstance(answer_send,str):
                api.send_msg.image(wxid,answer_send)
            elif isinstance(answer_send,dict):
                api.send_msg.image(wxid,**answer_send)
        case "File":
            if isinstance(answer_send,str):
                api.send_msg.file(wxid,answer_send)
            elif isinstance(answer_send,dict):
                api.send_msg.file(wxid,**answer_send)
        case "Gif":
            if isinstance(answer_send,str):
                api.send_msg.gif(wxid,answer_send)
            if isinstance(answer_send,dict):
                api.send_msg.gif(wxid,**answer_send)
        case "Url":
            if isinstance(answer_send,str):
                raise RuntimeError("Url发送方式仅支持dict")
            if isinstance(answer_send,dict):
                api.send_msg.url(wxid,**answer_send)
        case "xml":
            if isinstance(answer_send,str):
                api.send_msg.xml(wxid,answer_send)
            if isinstance(answer_send,dict):
                api.send_msg.xml(wxid,**answer_send)
        case "quote":
            if isinstance(answer_send,str):
                raise RuntimeError("quote发送方式仅支持dict")
            if isinstance(answer_send,dict):
                api.send_msg.quote(wxid,**answer_send)
        case "Fav":
            if isinstance(answer_send,str):
                try:
                    answer_send_int=int(answer_send)
                except ValueError as e:
                    raise RuntimeError(f"Fav发送中需传入可转为int的favLocalID:{e}")
                else:
                    api.send_msg.fav(wxid,answer_send_int)
            if isinstance(answer_send,dict):
                api.send_msg.fav(wxid,**answer_send)


    # if isinstance(an_,(str,int)) is True:

    #     send_msg.text(wxid,sql_row_an_replace(action_sql.an_replace.read(),an_))
    # elif isinstance(an_,(list)) is True:
    #     for x in an_:
    #         send_msg.text(wxid,sql_row_an_replace(action_sql.an_replace.read(),x))
    # else:
    #     send_msg.text(wxid,str(an_))
    return




#@func_timeout.func_set_timeout(30)
async def answer(wxid,wxid_group,qu):  #主调用
    data=data_read()
    #global an_
    #an_=None
    qu_xml=qu_xml_data=qu_reply_content=qu_reply_wxid=None
    if qu.find("<?xml") == 0:
        qu_xml=qu
        try:
            qu_xml_data=xmltodict.parse(qu)
            qu=qu_xml_data["msg"]['appmsg']['title']
            if "msg" in qu_xml_data:
                if 'appmsg' in qu_xml_data["msg"]:
                    if 'refermsg' in qu_xml_data["msg"]['appmsg']:
                        qu_reply_content=qu_xml_data["msg"]['appmsg']['refermsg']['content']
                        qu_reply_wxid=qu_xml_data["msg"]['appmsg']['refermsg']['chatusr']#如果是None是回复的消息与发送这条回复消息的人是一个人(注意由于提前已经定义为None，所以需要先行判断是否有qu_reply_content)
                #if 'img' in qu_xml_data["msg"]:
        except:  # noqa: E722
            pass

    #@识别
    if qu.find("@") == 0 and qu.find(" ") != -1:
        if wxid_group != "":
            own_inf=data["own_inf"]
            own_inf_roomNick=get_roomNick_in_chatroom(wxid,own_inf["userName"])
            print(f"@{own_inf_roomNick}")
            if qu.find(f"@{own_inf_roomNick}"+" ") != -1:
                qu=qu.replace(f"@{own_inf_roomNick}"+" ",":@")
            #print(qu)


    if wxid_group is not None:
        if qu_xml_data is not None:
            printmsg.rece(f"{wxid}({wxid_group}) >> {qu_xml_data}")
        else:
            printmsg.rece(f"{wxid}({wxid_group}) >> {qu}")
    else:
        if qu_xml_data is not None:
            printmsg.rece(f"{wxid} >> {qu_xml_data}")
        else:
            printmsg.rece(f"{wxid} >> {qu}")

    if wxid_group == "":
        isChatroom = False
    else:
        isChatroom = True
    global msg_l
    msg_l={"robotname":robotname,"qu":qu,"wxid":wxid,"wxid_group":wxid_group,"qu_xml":qu_xml,"qu_xml_data":qu_xml_data,"qu_reply_content":qu_reply_content,"qu_reply_wxid":qu_reply_wxid,'isChatroom': isChatroom}
    print(msg_l)

    # #admin部分
    # data=data_read()
    # wxid_admin=data["wxid_admin"]
    # if wxid in wxid_admin or wxid_group in wxid_admin:
    #     sql_row(row_qukey_admin)
    #     if an_ is not None:
    #         await send_msg_an()
    #         return

    block=data["wxid_block"]
    white=data["wxid_white"]
    if wxid  in block or wxid_group in block :    #黑名单
        return
    if len(white) != 0:
        if wxid not in white or wxid_group not in white:   #白名单
            return





    #plugin
    #print(plugins.items())
    for plugins_type, plugins_sec in plugins.items():
        match plugins_type:
            case "plugin_common":
                for plugin_name, plugin_class in plugins_sec.items():
                    plugin_result=plugin_class.main(msg_l)
                    if plugin_result is not None:
                        if isinstance(plugin_result,AnswerBase):
                            await send_msg_an(plugin_result)
                        elif isinstance(plugin_result,AnswerBaseList):
                            for answer_result_base in plugin_result.answers:
                                await send_msg_an(answer_result_base)
            case "plugin_admin":
                if msg_l["wxid"] in data["wxid_admin"]:
                    for plugin_name,plugin_class in plugins_sec:
                        plugin_result=plugin_class.main(msg_l)
                        if plugin_result is not None:
                            if isinstance(plugin_result,AnswerBase):
                                await send_msg_an(plugin_result)
                            elif isinstance(plugin_result,AnswerBaseList):
                                for answer_result_base in plugin_result.answers:
                                    await send_msg_an(answer_result_base)




    # #other部分
    # sql_row(row_qukey)
    # if an_ is not None :
    #     await send_msg_an()
    #     return
    #access接入部分
    # sql_row_access(row_access)
    # #print(an_)
    # if an_ is not None :
    #     await send_msg_an()
    #     return
    # return

    # #answerAPI部分
    # answer=API_answer(qu,wxid)
    # if 'status' in answer:
    #     st=answer['status']
    # if 'answer' in answer :
    #     an_=answer['answer']
    # if 'options' in answer:
    #         options=answer['options']
    #         an_=an_+ '  :  ' + str(options)

    # if an_ != None :
    #     send_msg.text_an()
    #     return


if __name__ == "__main__":
    qu=""


    #print(sys.argv)
    for x in sys.argv[3:]:
        qu=f"{qu} {x}"
    qu=qu.strip()
    #print(sys.argv[1],sys.argv[2],qu)

    #print(qu)
    try:
        print(answer(sys.argv[1],sys.argv[2],qu))
    except func_timeout.exceptions.FunctionTimedOut:
        printerr("Timeout-主函数执行超时(30s)")
        #send_msg.text("timeout-主函数执行超时")





