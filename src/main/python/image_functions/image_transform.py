import os
from datetime import datetime

import imagesize
import numpy as np
from skimage.io import imread
from skimage.transform import resize

from src.main.python.enviroment.enviroment_variables import NORMALIZE, BASEWIDTH, BASEHEIGHT, MIN_HEIGHT, MIN_WIDTH
from src.main.python.image_functions.image_object_json import imageObjectJson

normalize = NORMALIZE
basewidth = BASEWIDTH
baseheight = BASEHEIGHT
min_height = MIN_HEIGHT
min_width = MIN_WIDTH

def image_array(pixel_values):
    if normalize:
        return pixel_values / 255
    else:
        return pixel_values


def image_create(image_path):
    width, height = imagesize.get(image_path)
    pixel_values = reshape_image_invert(image_path, width, height)
    return imageObjectJson(os.path.basename(image_path),
                           datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                           pixel_values[1][0],
                           pixel_values[1][1],
                           image_array(pixel_values[0]))


def convert_to_gray(image):
    return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])


def reshape_image_invert(image_path, width, height):
    escala = escala_reducao(width, height)
    return np.array(resize(convert_to_gray(imread(image_path)), (escala[1], escala[0]))), escala


def escala_reducao(width, height):
    if width > basewidth:
        size_height = int((float(height) * float((basewidth / float(width)))))
        if size_height <= min_height or size_height is None:
            return basewidth, min_height
        else:
            return basewidth, size_height

    if height > baseheight:
        size_width = int((float(width) * float((baseheight / float(height)))))
        if size_width <= min_width or size_width is None:
            return min_width, baseheight
        else:
            return size_width, baseheight
    else:
        return width, height