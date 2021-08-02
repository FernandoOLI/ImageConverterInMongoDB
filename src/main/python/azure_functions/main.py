from azure.storage.blob import BlobServiceClient

from src.main.python.azure_functions.function import azure, container, AzureBlobFileDownloader, saveTmp, contador, mycol
from src.main.python.enviroment.enviroment_variables import PATH_BASE, ENVIROMENT
from src.main.python.image_functions.image_transform import image_create

enviroment = ENVIROMENT


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

    for blob in container_client.list_blobs():
        list_blob.append(blob)
        if count_download >= contador:
            azure_blob_file_downloader = AzureBlobFileDownloader()
            azure_blob_file_downloader.download_all_blobs_in_container(list_blob)
            saveTmp(blob_service_client)
            count_download = 0
            list_blob = []
        else:
            count_download = count_download + 1

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
