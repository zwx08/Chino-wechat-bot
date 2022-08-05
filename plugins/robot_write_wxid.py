from action_sql import plugins_sql, qu_key
from file_action import data_read, data_write_data


class another_data_write: #其他data.json的写入
    def admin(l):
        qu=l["qu"]
        qu_data=qu.splitlines()
        data=data_read()
        data["wxid_admin"].extend(qu_data[1:])
        data["wxid_admin"]=list(set(data["wxid_admin"]))
        data_write_data(data)
        data=data_read()
        d = [False for c in qu_data[1:] if c not in data["wxid_admin"]]
        if d:
            return 'error'
        else:
            return 'success'
    
    def block(l):
        qu=l["qu"]
        qu_data=qu.splitlines()
        
        data=data_read()
        data["wxid_block"].extend(qu_data[1:])
        data["wxid_block"]=list(set(data["wxid_block"]))
        data_write_data(data)
        data=data_read()
        d = [False for c in qu_data[1:] if c not in data["wxid_block"]]
        if d:
            return 'error'
        else:
            return 'success'
        
    def white(l):
        qu=l["qu"]
        qu_data=qu.splitlines()
        data=data_read()
        data["wxid_white"].extend(qu_data[1:])
        data["wxid_white"]=list(set(data["wxid_white"]))
        data_write_data(data)
        d = [False for c in qu_data[1:] if c not in data["wxid_white"]]
        if d:
            return 'error'
        else:
            return 'success'
        
        
if __name__ =='__main__':
    #插件信息写入
    plugins_sql.inf("robot_write_wxid",0.01,"zwx08","机器人配置写入——有关于wxid")
    qu_key.admin.write("robot_write_wxid_admin","&admin",1,'{plugin}.another_data_write.admin',1)
    qu_key.admin.write("robot_write_wxid_admin","&block",1,'{plugin}.another_data_write.block',1)
    qu_key.admin.write("robot_write_wxid_admin","&white",1,'{plugin}.another_data_write.white',1)
    
    
    