from domain.EnviromentVariables import PATH_BASE_SINGLE, PATH_BASE
from domain.functions import save, saveByPath, read


def image(path):
    save(path)

def images(path):
    saveByPath(path)

def readImage():
    read()

if __name__ == '__main__':
    image(PATH_BASE_SINGLE)
    #readImage()
    #images(PATH_BASE)
