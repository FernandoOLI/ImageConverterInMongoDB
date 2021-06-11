from domain.EnviromentVariables import PATH_BASE_SINGLE
from domain.functions import save, saveByPath

def image(path):
    save(path)

def images(path):
    saveByPath(path)

if __name__ == '__main__':
    image(PATH_BASE_SINGLE)
    #images(PATH_BASE)
