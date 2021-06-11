import os
from datetime import datetime

import numpy as np
from skimage.io import imread
from skimage.transform import resize

from domain.EnviromentVariables import CLIENT_DATABASE, DATABASE, COLLECTION, BASEWIDTH, BASEHEIGHT, MIN_HEIGHT, MIN_WIDTH, \
    NORMALIZE
from domain.imageObjectJson import imageObjectJson

import pymongo
import imagesize

#Variáveis de ambiente
myclient = pymongo.MongoClient(CLIENT_DATABASE)
mydb = myclient[str(DATABASE)]
mycol = mydb[str(COLLECTION)]
basewidth = BASEWIDTH
baseheight = BASEHEIGHT
min_height = MIN_HEIGHT
min_width = MIN_WIDTH
normalize = NORMALIZE


def image_array(pixel_values):
    if normalize:
        return pixel_values / 255
    else:
        return pixel_values


def image_create(image_path):
    width, height = imagesize.get(image_path)
    pixel_values = reshapeImageInvert(image_path, width, height)
    return imageObjectJson(os.path.basename(image_path),
                           datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                           pixel_values[1][0],
                           pixel_values[1][1],
                           image_array(pixel_values[0]))


def save(image):
    x = image_create(image).toJson()
    mycol.insert_one(x)


def saveMany(path, images):
    print("--- %s saveMany ---")
    import time
    start_time = time.time()
    list_image = []
    for image in images:
        save(path + image)
        #list_image.append(image_create(path + image).toJson())
    print("--- %s Processamento: seconds ---" % (time.time() - start_time))
    #start_time = time.time()
    #mycol.insert_many(list_image)
    #print("--- %s Save: seconds ---" % (time.time() - start_time))


def saveByPath(path):
    from os import walk
    _, _, filenames = next(walk(path))
    saveMany(path, filenames)


def convertToGray(image):
    return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])

def reshapeImageInvert(image_path, width, height):
    escala = escalaReducao(width, height)
    return np.array(resize(convertToGray(imread(image_path)), (escala[1], escala[0]))), escala


def escalaReducao(width, height):
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
