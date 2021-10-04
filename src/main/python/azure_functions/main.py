import os

from azure.storage.blob import BlobServiceClient

from src.main.python.azure_functions.function import azure, container, AzureBlobFileDownloader, saveTmp, contador, mycol
from src.main.python.enviroment.enviroment_variables import PATH_BASE, ENVIROMENT, QUANTIDADE, TEMP_PATH
from src.main.python.image_functions.image_transform import image_create
import numpy as np
from zipfile import ZipFile

enviroment = ENVIROMENT
quantidade = QUANTIDADE

def run_image():
    if enviroment == 'local':
        local_execute()
    elif enviroment == 'cluster':
        cluster_execute()
    else:
        print("error!")


def cluster_execute():
    blob_service_client = BlobServiceClient.from_connection_string(azure)
    container_client = blob_service_client.get_container_client(container=container)
    count_download = 0
    list_blob = []
    list_file = container_client.list_blobs()
    for blob in list_file:
        list_blob.append(blob)
        if count_download >= contador:
            azure_blob_file_downloader = AzureBlobFileDownloader()
            azure_blob_file_downloader.download_all_blobs_in_container(list_blob)
            saveTmp(blob_service_client)
            count_download = 0
            list_blob = []
        else:
            count_download = count_download + 1

    zip_download(list_file)
    if len(list_blob) > 0:
        saveTmp(blob_service_client)


def local_execute():
    saveByPath(PATH_BASE)


def saveMany(path, images):
    list_image = []
    count_limit = 0
    for image in images:
        list_image.append(image_create(path + image).toJson())
        if count_limit >= contador:
            mycol.insert_many(list_image)
            list_image = []
            count_limit = 0
        else:
            count_limit = count_limit + 1
    if len(list_image) > 0:
        mycol.insert_many(list_image)


def saveByPath(path):
    from os import walk
    _, _, filenames = next(walk(path))
    saveMany(path, filenames)


def main():
    print("Connect Azure")
    blob_service_client = BlobServiceClient.from_connection_string(azure)
    container_client = blob_service_client.get_container_client(container=container)
    list_file = container_client.list_blobs()
    zip_download(list_file)


tmp_path = TEMP_PATH
from os.path import basename
def zip_download(list_url):
    print("zip_download")
    quantidade_image = qnt_image(list_url)
    azure_blob_file_downloader = AzureBlobFileDownloader()
    print(list_url)
    azure_blob_file_downloader.download_all_blobs_in_container(list_url)

#    for x in np.random.choice(list_url, quantidade_image):
 #       os.path.join(tmp_path, x)
    import tkinter
    from tkinter import filedialog
    import os

    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window

    def search_for_file_path():
        currdir = os.getcwd()
        tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            print("You chose: %s" % tempdir)
        return tempdir

    file_path_variable = search_for_file_path()

    with ZipFile('sample.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(tmp_path):
            print(filenames)
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                print(filePath)
                # Add file to zip
                zipObj.write(filePath, basename(file_path_variable))


def qnt_image(list_url):
    if (len(list(list_url)) > quantidade):
        return quantidade
    else:
        return len(list(list_url))

