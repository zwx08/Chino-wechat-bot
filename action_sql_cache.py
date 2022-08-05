import sqlite3 as sqlite


def sql():
    con = None
    con = sqlite.connect('wx_cache.db',check_same_thread=False)
    return con

class base():
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
        
    def table_read(table,con=sql()):
        with con:
            con.row_factory = sqlite.Row
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            return rows