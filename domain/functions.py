import os
import uuid
from datetime import datetime
from io import BytesIO

import numpy as np
from azure.storage.blob import BlobServiceClient
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
    image_json = image_create(image).toJsonBinary()
    mycol.insert_one(image_json)

def read():
    #image_read = mycol.find_one({"data": "16/06/2021 14:51:53"})
    #print(list(image_read)[1])
    #image_read = mycol.find_one({"data": "16/06/2021 15:14:59"})
    #print(list(image_read))
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = "deltaimageconteiner"
    container_client = blob_service_client.get_container_client(container=container_name)
    for blob in container_client.list_blobs():
        print(blob)
        blob_client = container_client.get_blob_client(blob)
        print(blob_client.url)
        save(blob_client.url)
        #blob_client = container_client.get_blob_client(blob.name)
        #streamdownloader = blob_client.download_blob()
        #stream = BytesIO()
        #streamdownloader.download_to_stream(stream)
        #Image.open(byte_stream)
        #blob_service_client.get_blob_to_path(container_name, blob.name)


def database_to_object(object_database):
    print()

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
