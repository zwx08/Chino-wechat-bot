import logging
# time_out=time.strftime("%H:%M:%S", time.localtime())
# def standard_print(pri_content):
    # print(f"[{time_out}]{pri_content}")
class printmsg:
    @classmethod
    def send(cls,content:str):
        logging.info(f"[msg_send] {content}")
    @classmethod
    def rece(cls,content:str):
        logging.info(f"[msg_rece] {content}")
def printerr(content:str):
    logging.error(f"[Error] {content}")
def printinf(content:str):
    logging.info(f"[info] {content}")
def printres(content:str):
    logging.debug(f"[Response] {content}")
