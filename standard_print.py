import time,xmltodict
time_out=time.strftime("%H:%M:%S", time.localtime())
def standard_print(pri_content):
    print(f"[{time_out}]{pri_content}")
class printmsg():
    def send(content):
        standard_print(f"[msg_send] {content}")
    def rece(content):
        standard_print(f"[msg_rece] {content}")
def printerr(content):
    standard_print(f"[Error] {content}")
def printinf(content):
    standard_print(f"[info] {content}")
def printres(content):
    standard_print(f"[Response] {content}")
    