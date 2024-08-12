import logging
# time_out=time.strftime("%H:%M:%S", time.localtime())
# def standard_print(pri_content):
    # print(f"[{time_out}]{pri_content}")


from logging.handlers import RotatingFileHandler

# logger = logging.getLogger("Chino_old")

# file_handler = RotatingFileHandler(os.path.join(os.path.dirname(__file__),'app.log'), maxBytes=10000, backupCount=3)
# file_handler.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)


# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)

# logger.addHandler(file_handler)
# logger.addHandler(console_handler)


# 设置日志基础配置
logging.basicConfig(
    level=logging.DEBUG,  # 日志级别
    format='%(asctime)s [%(levelname)s] %(message)s',  # 日志格式
)

# 创建一个 rotating file handler，该handler可以将日志输出到文件，并在文件达到一定大小后进行切割
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5,encoding='utf-8')
logger = logging.getLogger(__name__)
logger.addHandler(handler)

class printmsg:
    @staticmethod
    def send(content:str):
        logger.info(f"[msg_send] {content}")
    @staticmethod
    def rece(content:str):
        logger.info(f"[msg_rece] {content}")
def printerr(content:str):
    logger.error(f"[Error] {content}")
def printinf(content:str):
    logger.info(f"[info] {content}")
def printres(content:str):
    logger.debug(f"[Response] {content}")
