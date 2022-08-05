import os
import yaml


class config():   #通用yaml文件
    def read(name):
        filename = os.path.join(os.path.dirname(__file__),'config',f'{name}.yaml').replace("\\","/")
        with open(filename, encoding='utf-8') as f:
            return yaml.safe_load(f)
    def write_yaml_a(name,a):
        filename = os.path.join(os.path.dirname(__file__),'config',f'{name}.yaml').replace("\\","/")
        with open(filename,"a",encoding='utf-8') as f:
            f.write(yaml.dump(a,allow_unicode=True))
    def write_a(name,a):
        filename = os.path.join(os.path.dirname(__file__),'config',f'{name}.yaml').replace("\\","/")
        with open(filename,"a",encoding='utf-8') as f:
            f.write(a)
    def write_yaml(name,w):
        filename = os.path.join(os.path.dirname(__file__),'config',f'{name}.yaml').replace("\\","/")
        with open(filename,"w",encoding='utf-8') as f:
            f.write(yaml.dump(w,allow_unicode=True))
            
    def first(name,first_content):
        filename = os.path.join(os.path.dirname(__file__),'config',f'{name}.yaml').replace("\\","/")
        try:
            with open(filename, 'x', encoding='utf-8') as file:
                file.write(first_content)
                file.close
        except:
            pass
            