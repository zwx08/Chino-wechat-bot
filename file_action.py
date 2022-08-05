import yaml,ujson

def config_read():
    with open('config.yaml', encoding='utf-8') as f:
        return yaml.safe_load(f)
        
def data_read():
    with open("wx_data.json",encoding="utf-8") as file:
        data_json = file.read() 
        file.close()
    data=ujson.loads(data_json)
    return data

def data_write_data(data):
    data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
    with open('wx_data.json', 'w', encoding='utf-8') as file:
        file.write(data_json)
        file.close()

def data_write(a,b_a,b_b):
    data=data_read()
    data[a][b_a]=b_b
    data_json=ujson.dumps(data, ensure_ascii=False, indent=4)
    with open('wx_data.json', 'w', encoding='utf-8') as file:    
        file.write(data_json)
        file.close()