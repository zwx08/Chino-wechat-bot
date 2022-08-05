from more_action import *
import imghdr
#data=get_QR_code()
#print(imghdr.what("",data))
with open("QR_code.png","wb") as file:
    file.write(get_QR_code())
    file.close

