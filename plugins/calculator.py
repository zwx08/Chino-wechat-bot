from sympy import *
from action_sql import plugins_sql, qu_key
import ujson
import action_sql_cache
from standard_print import printerr
from func_timeout import func_set_timeout
import func_timeout

def sym(l):
    qu=l["qu"]
    qu_data=qu.splitlines()
    sym=qu_data[3]
    sym_l=sym.split()
    for sym_l_ in sym_l:
        #print(f"{x}=symbols('%s')" % str(x))
        exec(f"{sym_l_}=symbols('%s')" % str(sym_l_))
    x, y, z ,a ,b ,c= symbols('x y z a b c')
    try:
        intr = solve(qu_data[1:2], sym_l)
    except SympifyError:
        return "错误"
    return intr


@func_set_timeout(30)
def calculator(l):
    qu=l["qu"]
    #wxid=l['wxid']
    
    calc = qu[3:]
    #with con:
    #    c = con.cursor()
    #    c.execute('''CREATE TABLE IF NOT EXISTS calc(
    #    wxid      TEXT    NOT NULL,
    #    cache     TEXT            ,
    #    PRIMARY KEY (wxid))''')
    #c = con.cursor()
    try:
        #if calc.find("s") != -1:
        #    try:
        #        c.execute(f"SELECT * FROM calc WHERE wxid={wxid}")
        #        save = c.fetchone()
        #        calc=calc.replace("s",save)
        #        an = str(solve(calc))
        #        c.execute(f"REPLACE INTO calc VALUES ('{wxid}','{an}')")
        #    except Exception as e:
        #        printerr(e)
        #        "Error"
        #else:
        an = str(eval(calc))
            
            #c.execute(f"REPLACE INTO calc VALUES ('{wxid}','{an}')")
    except:
        an="输入错误"
    #finally:
        #c.close()
        #con.close()
    return an
if __name__ =="__main__":
    plugins_sql.inf("calculator",0.01,"zwx08","计算器",)
    qu_key.write("calc","$c",1,"{plugin}.calculator",1,"计算器",Enabled=False)
    qu_key.write("calc_sym","$ym",1,"{plugin}.sym",1,"计算器_sym")