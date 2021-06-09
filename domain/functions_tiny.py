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
mycol = mydb["normalize_tiny"]


def image_array(pixel_values, width, height, channels):
    image = np.array(pixel_values).reshape((width, height, channels)) / 255
    return image


def image_create(image):

    return imageObjectJson("image tiny",
                           "RGB",
                           datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                           32,
                           32,
                           image)


def save(image):
    mycol.insert_one(image_create(image).toJson())


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
