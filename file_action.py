import yaml
import ujson
import os
wx_data_file=os.path.join(os.path.dirname(__file__),"wx_data.json")
config_file=os.path.join(os.path.dirname(__file__),"config.yaml")

def data_read():
    with open(wx_data_file,encoding="utf-8") as file:
        data_json = file.read()
        file.close()
    data=ujson.loads(data_json)
    return data

def data_write_data(data):
    data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
    with open(wx_data_file, 'w', encoding='utf-8') as file:
        file.write(data_json)
        file.close()

def data_write(a,b_a,b_b):
    data=data_read()
    data[a][b_a]=b_b
    data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
    with open(wx_data_file, 'w', encoding='utf-8') as file:
        file.write(data_json)
        file.close()