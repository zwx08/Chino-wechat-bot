# plugin 编写帮助

插件实现使用 pluginlib

## 定义

### 插件父类

```python
import pluginlib

@pluginlib.Parent('plugin_common', group='msg_plugin')
class plugin_common(object):

    @classmethod
    @pluginlib.abstractmethod
    def main(cls,msg_l):
        pass

@pluginlib.Parent('plugin_admin', group='msg_plugin')
class plugin_admin(object):   #有admin权限的人可用

    @classmethod
    @pluginlib.abstractmethod
    def main(cls,msg_l):
        pass
```

在收到一个消息的时候，会调用每一个插件中的 main 方法，传入 msg_l。当不为None的时候检测是AnswerBase类型还是AnswerBaseList类型，如果是其中之一则交给发送消息的部分

### msg_l 定义

```python
msg_l={"robotname":robotname,"qu":qu,"wxid":wxid,"wxid_group":wxid_group,"qu_xml":qu_xml,"qu_xml_data":qu_xml_data,"qu_reply_content":qu_reply_content,"qu_reply_wxid":qu_reply_wxid,'isChatroom': isChatroom}
```

群组中内容示例：

```json
{'robotname': '智乃', 'qu': '&ip', 'wxid': '20848218285@chatroom', 'wxid_group': 'wxid_3412raihkd6w22', 'qu_xml': None, 'qu_xml_data': None, 'qu_reply_content': None, 'qu_reply_wxid': None, 'isChatroom': True}
```

非群组中内容示例：

```json
{'robotname': '智乃', 'qu': '&ip', 'wxid': 'wxid_2eokvnwm9a5a22', 'wxid_group': '', 'qu_xml': None, 'qu_xml_data': None, 'qu_reply_content': None, 'qu_reply_wxid': None, 'isChatroom': False}
```

（qu 是消息内容）

### AnswerBase 定义

```python
class AnswerBase(BaseModel):
    answer: str | dict     # dict是直接解析到api中去的(主要是用来一些不止需要content的发送方式)，查看api_action.py
    # Replace: Optional[bool] = False
    # Replace_way: Optional[int] = 0
    send_way: Optional[Literal["Text","Image","File","Gif","Url","Xml","Quote","Fav"]] = "Text"
class AnswerBaseList(BaseModel):
    answers: List[AnswerBase]
```

Replace 说不定会删掉，别用。

## 示例插件

```python
import os
import sys
import httpx

from Chino_old.plugins_parser import plugin_common
from Chino_old.model_definition import AnswerBase

class ip(plugin_common):

    __version__='0.0.1'
    @classmethod
    def main(cls,msg_l)-> AnswerBase | None:
        qu=msg_l["qu"]
        if qu.find("&ip") != -1:
            if len(qu) <= 4:
                an = httpx.get('https://checkip.amazonaws.com').text.strip()
            else:
                an = cls.getting_ip(qu[4:])
            answer_model=AnswerBase(answer=an)
            return answer_model
        else:
            return None

    @staticmethod
    def getting_ip(args): #ip读取
        url = 'http://freeapi.ipip.net/' #中文免费
        url2 = 'http://ip-api.com/json/' #外国网站
        url=url+format(args)
        url2 = url2 + format(args)
        response = httpx.get(url)
        response2 = httpx.get(url2)

        str=response.text.replace('\"','') #去掉双引号
        str=str.replace('[','')      #去掉方括号
        str=str.replace(']','')
        str=str.replace(' ','')

        str=str.split(",")  #已逗号为分割符号，分割字符串为数组
        str[4] = str[4].replace('\n', '') #去掉回车符号

        strpp={}         #定义一个字典strpp
        strpp=response2.json()  #把英文网站json接口返回值传给字典strpp


        return f"""您查询的IP地址:{args})
        <www.ipip.net>
        国家:{str[0]}
        省份:{str[1]}
        城市:{str[2]}
        区域:{str[3]}
        运营商:{str[4]}"
        <www.ip-api.com>
        国家:{strpp.get('country')}
        城市:{strpp.get('city')}
        经纬度坐标:{strpp.get('lat')},{strpp.get('lon')}
        运营商编号:{strpp.get('as')}
        ISP服务商:{strpp.get('isp')}"""
```
