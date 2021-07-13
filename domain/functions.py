import os
import uuid
from datetime import datetime, timedelta
from io import BytesIO

import numpy as np
from azure.storage.blob import BlobServiceClient, BlobClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from skimage.io import imread
from skimage.transform import resize

from domain.EnviromentVariables import CLIENT_DATABASE, DATABASE, COLLECTION, BASEWIDTH, BASEHEIGHT, MIN_HEIGHT, \
    MIN_WIDTH, \
    NORMALIZE, CONTADOR, AZURE_CONNECTION, AZURE_CONTAINER, TEMP_PATH
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
contador = CONTADOR
azure = AZURE_CONNECTION
container = AZURE_CONTAINER
tmp_path = TEMP_PATH


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
    blob_service_client = BlobServiceClient.from_connection_string(azure)
    # Create a unique name for the container
    container_name = "deltaimageconteiner"
    container_client = blob_service_client.get_container_client(container=container_name)
    contador_download = 0
    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob.name)
        streamdownloader = blob_client.download_blob()
        stream = BytesIO()
        streamdownloader.download_to_stream(stream)

        if contador_download >= contador:
            azure_blob_file_downloader = AzureBlobFileDownloader()
            azure_blob_file_downloader.download_all_blobs_in_container()
            saveTmp(blob_service_client)
            contador_download = 0
        else:
            contador_download = contador_download + 1

    class AzureBlobFileDownloader:
        def __init__(self):
            print("Intializing AzureBlobFileDownloader")

            # Initialize the connection to Azure storage account
            self.blob_service_client = BlobServiceClient.from_connection_string(azure)
            self.my_container = self.blob_service_client.get_container_client(container)

        def save_blob(self, file_name, file_content):
            # Get full path to the file
            download_file_path = os.path.join(tmp_path, file_name)

            # for nested blobs, create local path as well!
            os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

            with open(download_file_path, "wb") as file:
                file.write(file_content)

        def download_all_blobs_in_container(self):
            my_blobs = self.my_container.list_blobs()
            for blob in my_blobs:
                print(blob.name)
                bytes = self.my_container.get_blob_client(blob).download_blob().readall()
                self.save_blob(blob.name, bytes)


    # Initialize class and upload files




def saveTmp(blob_service):
    print("--- %s saveMany ---")
    import time
    start_time = time.time()
    list_image = []
    contador_limite = 0
    from os import walk
    _, _, images = next(walk(tmp_path))

    for image in images:
        # save(path + image)
        list_image.append(image_create(tmp_path + image).toJson())
        if contador_limite >= contador:
            mycol.insert_many(list_image)
            list_image = []
            contador_limite = 0
            clearTmp()
        else:
            contador_limite = contador_limite + 1
    if len(list_image) > 0:
        mycol.insert_many(list_image)
    #clearTmp()
    move_azure_files(images, blob_service)
    print("---  Save: %s seconds ---" % (time.time() - start_time))

def move_azure_files(images, blob_service_client):

    source_container_name = 'deltaimageconteiner'
    target_container_name = "deltaimagebackup"
    account_name = 'deltaimage'
    for blob_name in images:

        source_blob = (f"https://{account_name}.blob.core.windows.net/{source_container_name}/{blob_name}")

        copied_blob = blob_service_client.get_blob_client(target_container_name, blob_name)
        copied_blob.start_copy_from_url(source_blob)

        remove_blob = blob_service_client.get_blob_client(source_container_name, blob_name)
        remove_blob.delete_blob()

def saveMany(path, images):
    print("--- %s saveMany ---")
    import time
    start_time = time.time()
    list_image = []
    contador_limite = 0
    for image in images:
        #save(path + image)
        list_image.append(image_create(path + image).toJson())
        if contador_limite >= contador:
            mycol.insert_many(list_image)
            list_image = []
            contador_limite = 0
            #clearTmp()
        else:
            contador_limite = contador_limite + 1
    if len(list_image) > 0:
        mycol.insert_many(list_image)
    #clearTmp()

    print("---  Save: %s seconds ---" % (time.time() - start_time))

def clearTmp():
    import shutil
    from os import path
    if path.exists(tmp_path):
        shutil.rmtree(tmp_path)
        os.mkdir(tmp_path, 0o777)
    else:
        os.mkdir(tmp_path, 0o777)

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
