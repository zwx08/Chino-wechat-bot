#qu_key：way：0= qu==keyword ，1=qu.find(keyword)
from inspect import getframeinfo, stack
import logging
import os
import ujson
import sqlite3 as sqlite



def sql():
    wx_db_file=os.path.join(os.path.dirname(__file__),"wx.db")
    con = sqlite.connect(wx_db_file,check_same_thread=False)
    logging.debug("SQL connect")
    return con
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class base():
    @classmethod
    def check_sql(cls,con=sql()):
        with con:
            c = con.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS plugins(
            NAME                  TEXT    NOT NULL,
            VERISON               TEXT            ,
            AUTHOR                TEXT            ,
            Explain               TEXT            ,
            Enabled               BLOB            ,
            filename              TEXT            )''')

            c.execute('''CREATE TABLE IF NOT EXISTS qu_key(
            NAME                  TEXT            ,
            keyword               TEXT            ,
            key_way               TEXT            ,
            answer                TEXT            ,
            an_way                TEXT            ,
            Explain               TEXT            ,
            Enabled               BLOB            ,
            filename              TEXT            ,
            help                  TEXT            )''')

            c.execute('''CREATE TABLE IF NOT EXISTS qu_key_admin(
            NAME                  TEXT            ,
            keyword               TEXT            ,
            key_way               TEXT            ,
            answer                TEXT            ,
            an_way                TEXT            ,
            Explain               TEXT            ,
            Enabled               BLOB            ,
            filename              TEXT            ,
            help                  TEXT            )''')

            c.execute('''CREATE TABLE IF NOT EXISTS an_replace(
            NAME                  TEXT            ,
            keyword               TEXT            ,
            key_way               TEXT            ,
            replace               TEXT            ,
            re_way                TEXT            ,
            Explain               TEXT            ,
            Enabled               BLOB            ,
            filename              TEXT            ,
            help                  TEXT            )''')

            c.execute('''CREATE TABLE IF NOT EXISTS Platform_access(
            NAME                  TEXT            ,
            access                TEXT            ,
            access_way            TEXT            ,
            Explain               TEXT            ,
            Enabled               BLOB            ,
            filename              TEXT            ,
            help                  TEXT            )''')



    @classmethod
    def empty_table(cls,table_name,con=sql()):
        with con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {table_name}")
            con.commit()
    @classmethod
    def del_table(cls,table_name,con=sql()):
        with con:
            cur = con.cursor()
            cur.execute(f"drop table {table_name}")
            con.commit()
    @classmethod
    def select_table(cls,con=sql()):
        with con:
            cur = con.cursor()
            cur.execute("""SELECT name FROM sqlite_master
                        WHERE type='table'
                        ORDER BY name;""")
            rows = cur.fetchall()
            return rows
    @classmethod
    def print_select_table_all(cls):
        row=base.select_table()
        for tab in row:
            rows=base.table_read(tab[0],con=sql())
            for rowss in rows:
                print(rowss[:])

    @classmethod
    def del_all_table(cls):
        row=base.select_table()
        for tab in row:
            base.del_table(tab[0])

    @classmethod
    def reset_table(cls):
        base.del_all_table()
        base.check_sql()
    @classmethod
    def table_read(cls,table,con=sql()):
        with con:
            con.row_factory = sqlite.Row
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            return rows




class plugins_sql():
    @classmethod
    def inf(cls,name,version=None,author=None,explain=None,Enabled=True,con=sql()):
        back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO plugins VALUES('{name}','{version}','{author}','{explain}','{Enabled}','{back_filename}')")
            con.commit()
    @classmethod
    def read(cls,con=sql()):
        with con as co:
            co.row_factory = sqlite.Row
            cur = co.cursor()
            cur.execute("SELECT * FROM plugins")
            rows = cur.fetchall()
            return rows

            for row in rows:
                print(f"{row['id']} {row['name']} {row['price']}")
class qu_key():
    @classmethod
    def _write(cls,table,name,keyword,key_way,answer,an_way,explain,help,Enabled,con):
        keyword=ujson.dumps(keyword)
        back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO {table} VALUES('{name}','{keyword}','{key_way}','{answer}','{an_way}','{explain}',{Enabled},'{back_filename}','{help}')")
    @classmethod
    def write(cls,name=None,keyword=None,key_way=0,answer=None,an_way=0,explain=None,help=None,Enabled=True,con=sql()):
        keyword=ujson.dumps(keyword)
        back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO qu_key VALUES('{name}','{keyword}','{key_way}','{answer}','{an_way}','{explain}',{Enabled},'{back_filename}','{help}')")
    @classmethod
    def read(cls,con=sql()):
        with con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM qu_key")
            rows = cur.fetchall()
            print(rows)
            return rows
            #for row in rows:
            #    print(f"{row['id']} {row['name']} {row['price']}")
    class admin:
        @classmethod
        def write(cls,name=None,keyword=None,key_way=0,answer=None,an_way=0,explain=None,help=None,Enabled=True,con=sql()):
            keyword=ujson.dumps(keyword)
            back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
            with con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO qu_key_admin VALUES('{name}','{keyword}','{key_way}','{answer}','{an_way}','{explain}',{Enabled},'{back_filename}','{help}')")
        @classmethod
        def read(cls,con=sql()):
            with con:
                con.row_factory = dict_factory
                cur = con.cursor()
                cur.execute("SELECT * FROM qu_key_admin")
                rows = cur.fetchall()
                return rows
                #for row in rows:
                #    print(f"{row['id']} {row['name']} {row['price']}")

class an_replace():
    @classmethod

    def write(cls,name=None,keyword=None,key_way=0,replace=None,re_way=0,explain=None,help=None,Enabled=True,con=sql()):
            back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
            with con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO an_replace VALUES('{name}','{keyword}','{key_way}','{replace}','{re_way}','{explain}',{Enabled},'{back_filename}','{help}')")
    @classmethod
    def read(cls,con=sql()):
        with con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM an_replace")
            rows = cur.fetchall()
            return rows
class access():
    @classmethod
    def write(cls,name=None,access=None,access_way=0,explain=None,help=None,Enabled=True,con=sql()):
            back_filename = os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]
            with con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO platform_access VALUES('{name}','{access}','{access_way}','{explain}',{Enabled},'{back_filename}','{help}')")

    @classmethod
    def read(cls,con=sql()):
        with con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM platform_access")
            rows = cur.fetchall()
            return rows

if __name__=="__main__":
    base.reset_table()