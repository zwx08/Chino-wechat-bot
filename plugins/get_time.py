import requests
import datetime

from Chino_old.plugins_parser import plugin_common
from Chino_old.model_definition import AnswerBase


class TimePlugin(plugin_common):


    _version_ ='0.1'
    @classmethod
    def main(cls,msg_l) -> AnswerBase | None:
        if msg_l["qu"].find("&getTime") != -1:

            # 获取服务器时间
            current_time = datetime.datetime.now()

            # 正确的格式化时间方式
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            return AnswerBase(answer=formatted_time,send_way="Text")
