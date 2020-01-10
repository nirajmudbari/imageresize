import base64
from PIL import Image
import cv2
from io import BytesIO
import numpy as np
import logging
from datetime import date

logging.basicConfig(filename='log.log', level=logging.ERROR)
today = date.today()
d2 = today.strftime("%B %d, %Y")

size = (900, 542)


def readb64(base64_string):
    try:
        sbuf = BytesIO()
        sbuf.write(base64.b64decode(base64_string))
        pimg = Image.open(sbuf)
        if not pimg.mode == 'RGB':
            pimg.convert('RGB')
        return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    except SystemError:
        logging.error(' | Date:' + d2 + ' | cannot parse base64 to image')


def imageToBase64(image):
    try:
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue())
        return img_str
    except SystemError:
        logging.error(' | Date:' + d2 + ' | cannot parse to base64')


def _is_big_enough(image, imagesize):
    if (image.shape[0] >= imagesize[0]) and (image.shape[1] >= imagesize[1]):
        return 1
    else:
        return 0


def _width_is_big_enough(image, width):
    if image.shape[1] >= width:
        return 1
    else:
        return 0


def _height_is_big_enough(image, height):
    if image.shape[0] >= height:
        return 1
    else:
        return 0


def getBase64ResizeAndReturnBase64(base64):
    try:
        cvimg = readb64(base64)
        print(cvimg.shape)
        heightresponse = _height_is_big_enough(cvimg, size[1])
        widthresponse = _width_is_big_enough(cvimg, size[0])
        valueresponse = _is_big_enough(cvimg, size)
        if valueresponse:
            print("image both height and width are ok")
            resized = cv2.resize(cvimg, size)
            img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            newbase64 = imageToBase64(im_pil)
            return newbase64
        elif heightresponse:
            print("image height is ok")
            if cvimg.shape[1] < 600:
                logging.error(' | Date:' + d2 + ' | cannot parse image as width is extreme low')
                print("cannot parse image as width is extreme low")
            else:
                print("width is scaledup")
                resized = cv2.resize(cvimg, size)
                img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(img)
                newbase64 = imageToBase64(im_pil)
                return newbase64
        elif widthresponse:
            print("image width is ok")
            if cvimg.shape[0] < 300:
                logging.error(' | Date:' + d2 + ' | cannot parse image as height is extreme low')
                print("cannot parse image as height is extreme low")
            else:
                print("height is scaledup")
                resized = cv2.resize(cvimg, size)
                img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(img)
                newbase64 = imageToBase64(im_pil)
                return newbase64
        elif (cvimg.shape[0] < 300 and cvimg.shape[1] < 600):
            logging.error(' | Date:' + d2 + ' | image is very small for tour')
            print("image is very small for tour")
        else:
            resized = cv2.resize(cvimg, (cvimg.shape[1], int(cvimg.shape[1] / 1.66)))
            img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            newbase64 = imageToBase64(im_pil)
            return newbase64
    except SystemError:
        logging.error(' | Date:' + d2 + ' | This is system exception')
