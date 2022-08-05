import subprocess
# -*- coding: utf-8 -
import os
from standard_print import printinf, printmsg
from action_sql import *

cur_path = os.path.dirname(os.path.realpath(__file__))# 当前脚本所在的文件绝对路径

os.putenv("PYTHONPATH", cur_path)# 将当前路径设置为python的临时环境变量，用于命令执行,需要设置是因为项目存在多处相互调用

def run_case():
    case_path = os.path.join(cur_path, "plugins")# 使用os.path.join拼接地址
    lst = os.listdir(case_path)# 获取当前目录下所有的文件名
    base.reset_table()
    for c in lst:
        # 判断文件名是以.py结尾的;添加and c.find("DemoGet") == -1就是去掉DemoGet.py文件
        if os.path.splitext(c)[1] == '.py' and c.find("__init__") == -1:
            # 查看文件名
            printinf(f"加载{c}")
            subprocess.Popen(['python',(os.path.join(case_path, c))],cwd=os.getcwd(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
if __name__ == "__main__":
    run_case()
    