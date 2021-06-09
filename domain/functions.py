import glob
import json
import os
from datetime import datetime

import numpy as np
from PIL import Image
import cv2

from domain import NumpyArrayEncoder
from domain.imageObjectJson import imageObjectJson

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["delta"]
mycol = mydb["normalize"]


def image_array(pixel_values, width, height, channels):
    image = np.array(pixel_values).reshape((width, height, channels)) / 255
    return image


def image_create(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "RGBA":
        channels = 4
    elif image.mode == "L":
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    return imageObjectJson(os.path.basename(image_path),
                           image.mode,
                           datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                           width,
                           height,
                           image_array(pixel_values, width, height, channels))


def save(image):
    import time
    start_time = time.time()
    x = image_create(image).toJson()
    print("--- %s Processamento: seconds ---" % (time.time() - start_time))
    mycol.insert_one(x)


def saveMany(path, images):
    print("--- %s saveMany ---")
    import time
    start_time = time.time()
    list_image = []
    for image in images:
        # save(path+image)
        x = image_create(path + image).toJson()
        file = open('out.txt', 'w')
        file.write(x.__str__())
        file.close()

        # print(x.__sizeof__())
        list_image.append(x)
    print("--- %s Processamento: seconds ---" % (time.time() - start_time))
    start_time = time.time()
    mycol.insert_many(list_image)
    print("--- %s Save: seconds ---" % (time.time() - start_time))


def saveByPath(path):
    from os import walk
    _, _, filenames = next(walk(path))
    saveMany(path, filenames)
