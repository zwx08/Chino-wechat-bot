import inspect
from another_action import *
from file_action import *
from answerAPI import *
import action_sql
import plugins
import wikipedia
from func_timeout import func_set_timeout
import func_timeout


def run_plugin(row,l):
    printinf(f"查询到qu_key{row['NAME']}")
    if row["an_way"] == "0":
        
        an=row["answer"]
    elif row["an_way"] == '1':
        #print(.411)
        Def=row["answer"]
        if Def.find("{plugin}") != -1:
            Def=Def.replace("{plugin}",f"plugins.{row['filename']}")
        try:
            an=eval(f"{Def}")(l)
        except func_timeout.exceptions.FunctionTimedOut:
            printerr("qu_key({row['NAME']})执行超时")
            an="超时-{row['NAME']}"
    return an
def keyword_(keyw,row,l):
    qu=l["qu"]
    if row["key_way"] == "0":
        #print(.21)
        if qu == keyw:
            #print(.31)
            an=run_plugin(row,l)
            return an

    elif row["key_way"] == "1":
        #print(.22)
        #qu=qu.replace(":@ ","",1)
        if qu.find(keyw) == 0:
            #print(.32)
            an=run_plugin(row,l)
            return an
    
    elif row["key_way"] == "2":
        #print(.23)
        if qu.find(keyw) != -1:
            #print(.33)
            an=run_plugin(row,l)
            return an
def sql_row(rows,l):
    for row in rows:
        #print(row)
        if row["Enabled"] == 'True':
            keyword=ujson.loads(row["keyword"])
            #printinf(keyword)
            if isinstance(keyword,(list)) ==True:
                for key_x in keyword:
                    an=keyword_(key_x,row,l)
            if isinstance(keyword,(str,int)) ==True:
                an=keyword_(keyword,row,l)
    return an

def answer_admin(l):
    qu=l["qu"]
    wxid=l["wxid"]
    wxid_group=l["wxid_group"]
    
    data=data_read()
    wxid_admin=data["wxid_admin"]
    if wxid in wxid_admin or wxid_group in wxid_admin:
        
        rows=action_sql.qu_key.admin.read()
        an_admin=sql_row(rows,l)

    if "an_admin" in vars():
        return an_admin
    

def answer_other(l):
    qu=l["qu"]
    wxid=l["wxid"]
    wxid_group=l["wxid_group"]
    
    rows=action_sql.qu_key.read()
    an=sql_row(rows,l)
    
    if "an" in vars() and "an" != None:
        return an

    



