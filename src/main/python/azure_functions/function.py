import os

from azure.storage.blob import BlobServiceClient

from src.main.python.enviroment.enviroment_variables import AZURE_CONNECTION, AZURE_CONTAINER, TEMP_PATH, AZURE_BACKUP, \
    AZURE_NAME
from src.main.python.image_functions.image_transform import image_create
from src.main.python.enviroment.enviroment_variables import CLIENT_DATABASE, DATABASE, COLLECTION, CONTADOR, AZURE_CONNECTION, AZURE_CONTAINER, TEMP_PATH
import pymongo

# Variáveis de ambiente
myclient = pymongo.MongoClient(CLIENT_DATABASE)
mydb = myclient[str(DATABASE)]
mycol = mydb[str(COLLECTION)]
tmp_path = TEMP_PATH

contador = CONTADOR
azure = AZURE_CONNECTION
container = AZURE_CONTAINER
backup = AZURE_BACKUP
azure_name = AZURE_NAME

class AzureBlobFileDownloader:
    def __init__(self):
        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(azure)
        self.my_container = self.blob_service_client.get_container_client(container)

    def save_blob(self, file_name, file_content):
        # Get full path to the file
        download_file_path = os.path.join(tmp_path, file_name)
        print(download_file_path)
        # for nested blobs, create local path as well!
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

        with open(download_file_path, "wb") as file:
            file.write(file_content)

    def download_all_blobs_in_container(self, list_blob):
        print("download_all_blobs_in_container", len(list(list_blob)))
        for blob in list_blob:
            bytes = self.my_container.get_blob_client(blob).download_blob().readall()
            self.save_blob(blob.name, bytes)


def save(image):
    image_json = image_create(image).toJsonBinary()
    mycol.insert_one(image_json)


def saveTmp(blob_service):
    list_image = []
    limit_count = 0
    from os import walk
    _, _, images = next(walk(tmp_path))

    for image in images:
        # save(path + image)
        list_image.append(image_create(tmp_path + image).toJson())
        if limit_count >= contador:
            mycol.insert_many(list_image)
            list_image = []
            limit_count = 0
            clearTmp()
        else:
            limit_count = limit_count + 1

    if len(list_image) > 0:
        mycol.insert_many(list_image)
        clearTmp()
    move_azure_files(images, blob_service)


def move_azure_files(images, blob_service_client):
    for blob_name in images:
        source_blob = (f"https://{azure_name}.blob.core.windows.net/{container}/{blob_name}")

        copied_blob = blob_service_client.get_blob_client(backup, blob_name)
        copied_blob.start_copy_from_url(source_blob)

        remove_blob = blob_service_client.get_blob_client(container, blob_name)
        remove_blob.delete_blob()

def clearTmp():
    import shutil
    from os import path
    if path.exists(tmp_path):
        shutil.rmtree(tmp_path)
        os.mkdir(tmp_path, 0o777)
    else:
        os.mkdir(tmp_path, 0o777)

def clear_backup():
    blob_service_client = BlobServiceClient.from_connection_string(azure)
    container_client = blob_service_client.get_container_client(container=backup)
    for blob_name in container_client.list_blobs():
        remove_blob = blob_service_client.get_blob_client(backup, blob_name)
        remove_blob.delete_blob()

