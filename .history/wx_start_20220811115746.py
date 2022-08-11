#linux系统注意，请确定已经配置完成wine环境以及配置好图形化界面，且请于图形化界面执行此文件
#windows系统未进行代码测试
import json
import os,subprocess,sys,termios
from time import sleep
from more_action import *
from goto import with_goto,goto,label

from standard_print import printerr, printinf
from io import BytesIO
from PIL import Image
import qrcode
def pre_posix():
    fd = sys.stdin.fileno()# 获取标准输入的描述符
    old_ttyinfo = termios.tcgetattr(fd)# 获取标准输入(终端)的设置
    new_ttyinfo = old_ttyinfo[:]# 配置终端
    new_ttyinfo[3] &= ~termios.ICANON# 使用非规范模式(索引3是c_lflag 也就是本地模式)
    new_ttyinfo[3] &= ~termios.ECHO# 关闭回显(输入不会被显示)
    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)# 使设置生效
    print(ord(os.read(fd, 7)))# 从终端读取
    return


def success():
    with open("status_wx_start","w") as file:
        file.write("success")


def QR_code():
    req=get_QR_code()
    qrcode_=Image.open(BytesIO(req.content))
    fileName="wechat_QRcode"+'.'+qrcode_.format.lower()
    cache=os.path.join(os.getcwd(),"cache",fileName)
    with open(cache,'wb') as f:
        f.write(req.content)
    qrcode.main(cache)
    return cache
@with_goto
def logging():
    name=os.name
    if name == "posix":
        label .run_posix
        printinf("执行启动")
        subprocess.Popen(["wine","./wx/wxdriver_cli.exe"])
        sleep(5)
        printinf("请手动执行登录，登录成功后输入任意字符")
        if check_wxchat_logging() == 0:
            qrcode_cache=QR_code()
            
            printinf(f"二维码位于:{qrcode_cache}")
            
        label .pre_posix
        pre_posix()
        check=json.loads(check_wxchat_logging())
        if check["login"] == 1:
            printinf("检测到登录成功")
            return
        elif check["login"] == 0:
            printinf("检测到未完成登录")
            goto .pre_posix
        else:
            printerr("无法检测登录状态，似乎并未启动成功,键入任意字符后重新执行启动")
            pre_posix()
            goto .run_posix
            
    elif name == "nt":   
        label .run_nt
        printinf("执行启动")
        subprocess.Popen(["./wx/wxdriver_cli.exe"])
        sleep(5)
        printinf("请手动执行登录，登录成功后输入任意字符")
        label .pre_nt
        input()
        check=json.loads(check_wxchat_logging())
        if check["login"] == 1:
            printinf("检测到登录成功")
            return
        elif check["login"] == 0:
            printinf("检测到未完成登录")
            goto .pre_nt
        else:
            printerr("无法检测登录状态，似乎并未启动成功,键入任意字符后重新执行启动")
            pre_posix()
            goto .run_nt
        
    else:
        printerr("不支持的系统")
        os.exit
        
        
if __name__ == "__main__":
    logging()