import action_sql 
#from plugins import *
import plugins
#action_sql.base.del_table("plugins")
def main():
    qu="&ip"
    wxid=1
    wxid_group=1
    Def='ip.start'
    print(eval(f"plugins.{Def}")({"qu":qu,"wxid":wxid,"wxid_group":wxid_group}))
    return
    rows=action_sql.qu_key.read()
    for row in rows:
        if row[5] == 'True':
            if row[3] == 0:
                if qu == row[1]:
                    print(f"查询到{row[0]}")
                    Def = row[2]
                    an=eval(f"plugins.{Def}")({"qu":qu,"wxid":wxid,"wxid_group":wxid_group})
            elif row[3] == 1:
                if qu.find(row[1]) != -1:
                    print(f"查询到{row[0]}")
                    Def = row[2]
                    an=eval(f"plugins.{Def}")({"qu":qu,"wxid":wxid,"wxid_group":wxid_group})
                    
#print(an)

def ip():
    action_sql.qu_key.write("ip","&ip",1,"ip.start",1,"ip查询")
if __name__ =="__main__":
    ip()