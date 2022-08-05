import subprocess
from standard_print import printinf
from wx_start import logging
from more_action import *
from goto import with_goto,goto,label

@with_goto
def check():
    label .inp
    inpu=input("请输入您的微信启动&注入方式:(自行启动&注入或已经启动&注入:m / 通过程序启动&注入:d)  (m/d):")
    printinf(inpu)
    if inpu == "d":
        logging()
        return
    elif inpu == "m":
        label .che
        printinf("检查中.....")
        try:
            check=json.loads(check_wxchat_logging())
            if check["login"] == 1:
                printinf("登录成功")
                return
            else:
                printinf("未登录,输入任意字符以重新检查是否启动并登录")
                input()
                goto .che
        except:
            printinf("连接失败,输入任意字符以重新检查是否启动并登录")
            input()
            goto .che
    else:
        goto .inp
        
if __name__ == "__main__":
    check()
    print("执行前置加载")
    subprocess.run(["python","./preload.py"])
    print("执行插件加载")
    subprocess.run(["python","./load_plugins.py"])
    print("执行server启动")
    subprocess.run(["python","./http_server.py"])