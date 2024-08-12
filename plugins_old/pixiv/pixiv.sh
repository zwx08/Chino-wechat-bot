import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {'Referer': 'https://www.pixiv.net/'}
url = 'https://i.pximg.net/img-original/img/2019/11/22/00/00/13/77926406_p0.jpg'
res = requests.get(url, headers=headers, verify=False)
with open('test.jpg', 'wb') as f:
    f.write(res.content)




