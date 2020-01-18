import base64

from PIL import Image
import io
import time
import logging
from datetime import date
from resizeimage import resizeimage
import os

logging.basicConfig(filename='resizelog.log', level=logging.ERROR)
today = date.today()
d2 = today.strftime("%B %d, %Y")

size = (900, 542)


def _is_big_enough(image, imagesize):
    if (image.size[0] >= imagesize[0]) and (image.size[1] >= imagesize[1]):
        return 1
    else:
        return 0


def _width_is_big_enough(image, width):
    if image.size[0] >= width:
        return 1
    else:
        return 0


def _height_is_big_enough(image, height):
    if image.size[1] >= height:
        return 1
    else:
        return 0


def decode_img(msg):
    try:
        if msg.startswith('data:') and ';base64' in msg:
            msg = msg.split(",")[1]
            msg = base64.b64decode(msg)
            buf = io.BytesIO(msg)
            img = Image.open(buf)
            return img

    except SystemError:
        logging.error(' | Date:' + d2 + ' | cannot parse base64 to image')


def image_to_base64():
    image = open('bbbb.png', 'rb')
    image_read = image.read()
    image_64_encode = b'data:image/png;base64,' + base64.b64encode(image_read)
    image_encoded = image_64_encode.decode('utf-8')
    return image_encoded


def removefile():
    if os.path.exists("bbbb.png"):
        os.remove("bbbb.png")


def getimageandreturnbase64(pilimage, size):
    resized = resizeimage.resize_contain(pilimage, size, resample=Image.LANCZOS, bg_color=(255, 255, 255, 0))
    fill_color = '#ffffff'
    if resized.mode in ('RGBA', 'LA'):
        # background = Image.new(resized.mode[:-1], resized.size, fill_color)
        # background.paste(resized, resized.split()[-1])
        # img = background
        resized.save('bbbb.png')
        time.sleep(1)
        newbase64 = image_to_base64()
        removefile()
        return newbase64
    else:
        resized.save('bbbb.png', quality=95)
        time.sleep(2)
        newbase64 = image_to_base64()
        removefile()
        return newbase64


def getBase64ResizeAndReturnBase64(base64):
    try:
        decodedimg = decode_img(base64)
        print(decodedimg.size)
        heightresponse = _height_is_big_enough(decodedimg, size[1])
        widthresponse = _width_is_big_enough(decodedimg, size[0])
        valueresponse = _is_big_enough(decodedimg, size)

        if valueresponse:
            print('both height and width are ok')
            return getimageandreturnbase64(decodedimg, size)
        # elif heightresponse:
        #     print("image height is ok")
        #     if decodedimg.size[0] < 600:
        #         logging.error(' | Date:' + d2 + ' | cannot parse image as width is extreme low')
        #         return None
        #     else:
        #         print("width is scaledup")
        #         return getimageandreturnbase64(decodedimg, size)
        #
        # elif widthresponse:
        #     print("image width is ok")
        #     if decodedimg.size[1] < 300:
        #         logging.error(' | Date:' + d2 + ' | cannot parse image as height is extreme low')
        #         return None
        #     else:
        #         print("height is scaledup")
        #         return getimageandreturnbase64(decodedimg, size)
        else:
            print("original image size")
            return getimageandreturnbase64(decodedimg, decodedimg.size)

    except SystemError:
        logging.error(' | Date:' + d2 + ' | This is system exception')
