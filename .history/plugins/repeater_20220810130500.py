from action_sql import access, plugins_sql


def main(l):
    print(1)
    return l["qu"]

if __name__=="__main__":
    plugins_sql.inf("repeater","0.0.1","zwx08","repeater")
    access.write("repeater","{plugin}.main",0,"复读机")
    