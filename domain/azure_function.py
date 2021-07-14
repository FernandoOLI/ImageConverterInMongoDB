import os

from azure.storage.blob import BlobServiceClient, BlobClient, generate_account_sas, ResourceTypes, AccountSasPermissions

from domain.EnviromentVariables import AZURE_CONNECTION, AZURE_CONTAINER, TEMP_PATH

azure = AZURE_CONNECTION
container = AZURE_CONTAINER
tmp_path = TEMP_PATH

class AzureBlobFileDownloader:
    def __init__(self):
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

    def download_all_blobs_in_container(self, list_blob):
        my_blobs = list_blob
        for blob in my_blobs:
            bytes = self.my_container.get_blob_client(blob).download_blob().readall()
            self.save_blob(blob.name, bytes)
