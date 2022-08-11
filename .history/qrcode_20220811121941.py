import os
from PIL import Image
from io import BytesIO
from more_action import check_wxchat_logging, get_QR_code
from standard_print import printinf

from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
def main(cache):
    barcode_url = ''
    barcodes = decode(Image.open(cache))
    for barcode in barcodes:
        barcode_url = barcode.data.decode("utf-8")
    print(barcode_url)

    qr = qrcode.QRCode()
    qr.add_data(barcode_url)
    #invert=True白底黑块,有些app不识别黑底白块.
    qr.print_ascii(invert=True)

def QR_code():
    req=get_QR_code()
    qrcode_=Image.open(BytesIO(req.content))
    fileName="wechat_QRcode"+'.'+qrcode_.format.lower()
    cache=os.path.join(os.getcwd(),"cache",fileName)
    with open(cache,'wb') as f:
        f.write(req.content)
    main(cache)
    return cache
                
            


if __name__ == '__main__':
    if check_wxchat_logging() == 0:
        qrcode_cache=QR_code()
        printinf(f"二维码位于:{qrcode_cache}")