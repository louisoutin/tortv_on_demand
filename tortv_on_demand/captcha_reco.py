import cv2
import numpy as np
import pkg_resources


def template_location(image: str, template_number: int, method: str = 'cv2.TM_CCOEFF_NORMED', threshold: float = 0.8):
    method = eval(method)
    img = cv2.imread(image, 0)
    stream = pkg_resources.resource_stream(__name__, 'templates/'+str(template_number)+'.png')
    file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    template = cv2.imdecode(file_bytes, 0)
    res = cv2.matchTemplate(img, template, method)
    loc = np.where(res >= threshold)
    return list(loc[1])


def read_captcha(image_path: str):
    captcha = []
    for i in range(10):
        res = template_location(str(image_path), i)
        captcha += [(r, i) for r in res]
    captcha.sort(key=lambda tup: tup[0])  # sorts in place
    str_res = ""
    for c in captcha:
        str_res += str(c[1])
    return str_res
    

# Usage example:
# read_captcha('captcha.jpg', './templates/') 
# This return a string with the 4 characters of the captcha (ex: "8563")
