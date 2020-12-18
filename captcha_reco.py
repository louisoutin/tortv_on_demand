import cv2
import numpy as np
from pathlib import Path
import numpy as np


def template_location(image:str, template:str, method:str='cv2.TM_CCOEFF', threshold:float =0.8):
    method = eval(method)
    img = cv2.imread(image,0)
    template = cv2.imread(template,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return list(loc[1])

def read_captcha(image_path:str, template_folder: str):
    captcha = []
    templates_imgs = [x for x in Path(template_folder).iterdir() if x.suffix == ".png"]
    templates_imgs.sort()
    for i, template_path in enumerate(templates_imgs):
        res = template_location(str(image_path), str(template_path))
        captcha += [(r, i) for r in res]
    captcha.sort(key=lambda tup: tup[0])  # sorts in place
    str_res = ""
    for c in captcha:
        str_res += str(c[1])
    return str_res
    

# Usage example:
# read_captcha('captcha.jpg', './templates/') 
# This return a string with the 4 characters of the captcha (ex: "8563")
