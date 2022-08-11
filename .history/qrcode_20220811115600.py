from PIL import Image

#计算每个方块的大小像素
def get_cell_size(x,y,x2,y2):
    for j in range(x,x2):
        for i in range(y,y2):
            pix = im.getpixel((j,i))
            if pix[:3]==(255,255,255):
                return j - x  #每个黑色格子的像素点大小
                
def get_cell():
    flag = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pix = im.getpixel((x,y))

            if pix[:3]==(0,0,0) and flag==0: #出现第一个黑色像素
                x1=x
                flag = 1
                
            if pix[:3]==(255,255,255) and flag ==1 : #出现第一个白色像素（意味着左上角的标记方块横向结束）
                flag = 2
                cell = get_cell_size(x1,x1,x,x)
                return cell
                
def get_qrcode(cell):
    height = int(HEIGHT/cell)
    width = int(WIDTH/cell)
    code=''
    for y in range(height):
        
        for x in range(width):
            pix = im.getpixel((x*cell,y*cell))
            if pix[:3]==(0,0,0):
                code += '▇'
            if pix[:3]==(255,255,255):
                code += '　'
        code += '\n'
    print(code)
    input('...')
                
            
def main(IMG):
    im = Image.open(IMG)
    WIDTH = im.width
    HEIGHT = im.height
    get_qrcode(get_cell())

if __name__ == '__main__':
    IMG = '123.png'
    im = Image.open(IMG)
    WIDTH = im.width
    HEIGHT = im.height
    get_qrcode(get_cell())
