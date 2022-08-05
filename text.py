from more_action import *
import sys
from PIL import Image
import numpy as np
import os

def main(file):
    img = np.array(Image.open(file).convert('L'), 'f')
    img1=np.zeros(shape=[51,51])
    img1=img[0:img.shape[0]:5,0:img.shape[1]:5]
    img1=img1//37

    for i in range(51):
        str = "echo "
        for j in range(51):
            if img1[i,j]==0:
                str=str+'\x1b[41;31m  '
            elif img1[i,j]==1:
                str=str+'\x1b[42;31m  '
            elif img1[i,j]==2:
                str=str+'\x1b[43;31m  '
            elif img1[i,j]==3:
                str=str+'\x1b[44;31m  '
            elif img1[i,j]==4:
                str=str+'\x1b[45;31m  '
            elif img1[i,j]==5:
                str=str+'\x1b[46;31m  '
            elif img1[i, j] == 6:
                str = str + '\x1b[47;31m  '
        str = str + '\x1b[0m'
        os.system(str)

if __name__=="__main__":
    
    
    x=ujson.loads(get_QR_code_URL())
    url=x['data']
    print(url)
    r = httpx.get(url)
    with open('QR_code.jpg','wb') as f:
        f.write(r)
        f.close()
    main('QR_code.jpg')