from action_sql import access, plugins_sql
from more_action import send_msg


def main(l):
    send_msg(l["wxid",l["qu"])

if __name__=="__main__":
    plugins_sql.inf("repeater","0.0.1","zwx08","repeater")
    access.write("repeater","{plugin}.main",0,"复读机")
    