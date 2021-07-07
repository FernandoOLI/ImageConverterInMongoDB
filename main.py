import pymongo

from domain.EnviromentVariables import PATH_BASE_SINGLE, PATH_BASE
from domain.functions import save, saveByPath, read


def image(path):
    save(path)

def images(path):
    saveByPath(path)

def readImage():
    read()

def testConection():
    client = pymongo.MongoClient(
        "mongodb+srv://user_app:N13fyjsqJvJ99bsu@cluster0.8kxb6.mongodb.net/delta?retryWrites=true&w=majority")
    db = client.test

if __name__ == '__main__':
    testConection()
    image(PATH_BASE_SINGLE)
    #readImage()
    #images(PATH_BASE)
