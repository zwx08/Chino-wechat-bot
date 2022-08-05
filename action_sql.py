#!/usr/bin/python
#qu_key：way：0= qu==keyword ，1=qu.find(keyword)
from inspect import getframeinfo, stack
import os,ujson
import sqlite3 as sqlite
import sys

def sql():
    con = None
    con = sqlite.connect('wx.db',check_same_thread=False)
    #printinf("wx数据库打开成功")
    return con
def dict_factory(cursor, row):  
    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d  

class base():
    def check_sql(con=sql()):
        with con:
            c = con.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS plugins(
            NAME                  TEXT    NOT NULL,
            VERISON               TEXT            ,
            AUTHOR                TEXT            ,
            Explain               TEXT            ,
            Enabled               TEXT            ,
            filename              TEXT            )''')

            c.execute('''CREATE TABLE IF NOT EXISTS qu_key(
            NAME                  TEXT            ,
            keyword               TEXT            ,
            key_way               TEXT            ,
            answer                TEXT            ,
            an_way                TEXT            ,
            Explain               TEXT            ,
            Enabled               TEXT            ,
            filename              TEXT            ,
            help                  TEXT            )''')

            c.execute('''CREATE TABLE IF NOT EXISTS qu_key_admin(
            NAME                  TEXT            ,
            keyword               TEXT            ,
            key_way               TEXT            ,
            answer                TEXT            ,
            an_way                TEXT            ,
            Explain               TEXT            ,
            Enabled               TEXT            ,
            filename              TEXT            ,
            help                  TEXT            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS an_replace(
            NAME                  TEXT            ,
            keyword               TEXT            ,
            key_way               TEXT            ,
            replace               TEXT            ,
            re_way                TEXT            ,
            Explain               TEXT            ,
            Enabled               TEXT            ,
            filename              TEXT            ,
            help                  TEXT            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS Platform_access(
            NAME                  TEXT            ,
            access                TEXT            ,
            access_way            TEXT            ,
            Explain               TEXT            ,
            Enabled               TEXT            ,
            filename              TEXT            ,
            help                  TEXT            )''') 
            
            
            

    def empty_table(table_name,con=sql()):
        with con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {table_name}")
            con.commit()
    def del_table(table_name,con=sql()):
        with con:
            cur = con.cursor()
            cur.execute(f"drop table {table_name}")
            con.commit()
    def select_table(con=sql()):
        with con:
            cur = con.cursor()
            cur.execute("""SELECT name FROM sqlite_master
                        WHERE type='table'
                        ORDER BY name;""")
            rows = cur.fetchall()
            return rows
    def print_select_table_all():
        row=base.select_table()
        for tab in row:
            rows=base.table_read(tab[0],con=sql())
            for rowss in rows:
                print(rowss[:])
        
        
    def del_all_table():
        row=base.select_table()
        for tab in row:
            base.del_table(tab[0])
            
    def reset_table():
        base.del_all_table()
        base.check_sql()
        
    def table_read(table,con=sql()):
        with con:
            con.row_factory = sqlite.Row
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            return rows
        
            
            
            
class plugins_sql():
    def inf(name,version=None,author=None,explain=None,Enabled=True,con=sql()):
        back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO plugins VALUES('{name}','{version}','{author}','{explain}','{Enabled}','{back_filename}')")
            con.commit()
    def read(con=sql()):
        with con as co:
            co.row_factory = sqlite.Row
            cur = co.cursor()
            cur.execute("SELECT * FROM plugins")
            rows = cur.fetchall()
            return rows
        
            for row in rows:
                print(f"{row['id']} {row['name']} {row['price']}")
class qu_key():
    def _write(table,name,keyword,key_way,answer,an_way,explain,help,Enabled,con):
        keyword=ujson.dumps(keyword)
        back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO {table} VALUES('{name}','{keyword}','{key_way}','{answer}','{an_way}','{explain}','{Enabled}','{back_filename}','{help}')")
    def write(name=None,keyword=None,key_way=0,answer=None,an_way=0,explain=None,help=None,Enabled=True,con=sql()):
        keyword=ujson.dumps(keyword)
        back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO qu_key VALUES('{name}','{keyword}','{key_way}','{answer}','{an_way}','{explain}','{Enabled}','{back_filename}','{help}')")
    def read(con=sql()):
        with con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM qu_key")
            rows = cur.fetchall()
            return rows
            #for row in rows:
            #    print(f"{row['id']} {row['name']} {row['price']}")
    class admin:
        def write(name=None,keyword=None,key_way=0,answer=None,an_way=0,explain=None,help=None,Enabled=True,con=sql()):
            keyword=ujson.dumps(keyword)
            back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
            with con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO qu_key_admin VALUES('{name}','{keyword}','{key_way}','{answer}','{an_way}','{explain}','{Enabled}','{back_filename}','{help}')")
        def read(con=sql()):
            with con:
                con.row_factory = dict_factory
                cur = con.cursor()
                cur.execute("SELECT * FROM qu_key_admin")
                rows = cur.fetchall()
                return rows
                #for row in rows:
                #    print(f"{row['id']} {row['name']} {row['price']}")

class an_replace():
    def write(name=None,keyword=None,key_way=0,replace=None,re_way=0,explain=None,help=None,Enabled=True,con=sql()):
            back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
            with con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO an_replace VALUES('{name}','{keyword}','{key_way}','{replace}','{re_way}','{explain}','{Enabled}','{back_filename}','{help}')")
    def read(con=sql()):
        with con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM an_replace")
            rows = cur.fetchall()
            return rows
class access():
    def write(name=None,access=None,access_way=0,explain=None,help=None,Enabled=True,con=sql()):
            back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
            with con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO platform_access VALUES('{name}','{access}','{access_way}','{explain}','{Enabled}','{back_filename}','{help}')")
    def read(con=sql()):
        with con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM platform_access")
            rows = cur.fetchall()
            return rows

if __name__=="__main__":
    base.reset_table()