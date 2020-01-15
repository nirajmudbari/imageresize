import base64

from PIL import Image
import cv2
import io
from io import BytesIO
import numpy as np
import logging
from datetime import date
from resizeimage import resizeimage

logging.basicConfig(filename='log.log', level=logging.ERROR)
today = date.today()
d2 = today.strftime("%B %d, %Y")

size = (900, 542)


def readb64(base64_string):
    try:
        if base64_string.startswith('data:') and ';base64' in base64_string:
            formattedbase64 = base64_string.split(",")[1];
            sbuf = BytesIO()
            sbuf.write(base64.b64decode(formattedbase64))
            pimg = Image.open(sbuf)
            if not pimg.mode == 'RGB':
                pimg.convert('RGB')
            return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    except SystemError:
        logging.error(' | Date:' + d2 + ' | cannot parse base64 to image')


def imageToBase64(image):
    try:
        fill_color = '#ffffff'
        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, fill_color)
            background.paste(image, image.split()[-1])
            img = background
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue())
            return b'data:image/png;base64,' + img_str
        else:
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue())
            return b'data:image/png;base64,' + img_str
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


def decode_img(msg):
    try:
        if msg.startswith('data:') and ';base64' in msg:
            msg = msg.split(",")[1];
            msg = base64.b64decode(msg)
            buf = io.BytesIO(msg)
            img = Image.open(buf)
            return img

    except SystemError:
        logging.error(' | Date:' + d2 + ' | cannot parse base64 to image')


def getBase64ResizeAndReturnBase64(base64):
    try:
        cvimg = readb64(base64)
        print(cvimg.shape)
        heightresponse = _height_is_big_enough(cvimg, size[1])
        widthresponse = _width_is_big_enough(cvimg, size[0])
        valueresponse = _is_big_enough(cvimg, size)
        if valueresponse:
            print("image both height and width are ok")
            img = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            im_pil.thumbnail(size, Image.LANCZOS, reducing_gap=2.0)
            im_pil.show()
            newbase64 = imageToBase64(im_pil)
            print(newbase64)
            return newbase64
        elif heightresponse:
            print("image height is ok")
            if cvimg.shape[1] < 600:
                logging.error(' | Date:' + d2 + ' | cannot parse image as width is extreme low')
            else:
                print("width is scaledup")
                img = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(img)
                im_pil.thumbnail(size, Image.LANCZOS, reducing_gap=2.0)
                newbase64 = imageToBase64(im_pil)
                return newbase64
        elif widthresponse:
            print("image width is ok")
            if cvimg.shape[0] < 300:
                logging.error(' | Date:' + d2 + ' | cannot parse image as height is extreme low')
            else:
                print("height is scaledup")
                img = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(img)
                im_pil.thumbnail(size, Image.LANCZOS, reducing_gap=2.0)
                newbase64 = imageToBase64(im_pil)
                return newbase64
        elif (cvimg.shape[0] < 300 and cvimg.shape[1] < 600):
            logging.error(' | Date:' + d2 + ' | image is very small for tour')
        else:
            img = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            im_pil.thumbnail(size, Image.LANCZOS, reducing_gap=2.0)
            newbase64 = imageToBase64(im_pil)
            return newbase64
    except SystemError:
        logging.error(' | Date:' + d2 + ' | This is system exception')


def image_to_base64():
    # img = Image.open(r'bbbb.jpg')
    image = open('bbbb.jpg', 'rb')
    image_read = image.read()

    # Get the Byte-Version of the image
    image_64_encode = base64.b64encode(image_read)

    # Convert it to a readable utf-8 code (a String)
    image_encoded = image_64_encode.decode('utf-8')
    return image_encoded


def newlogicforimage(base64):
    pilimage = decode_img(base64)
    resized = resizeimage.resize_thumbnail(pilimage, size, resample=Image.LANCZOS)
    fill_color = '#ffffff'
    if resized.mode in ('RGBA', 'LA'):
        background = Image.new(resized.mode[:-1], resized.size, fill_color)
        background.paste(resized, resized.split()[-1])
        img = background
        img.save('bbbb.jpg', quality=95)
        newbase64 = image_to_base64()
        return newbase64
