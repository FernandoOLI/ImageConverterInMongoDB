from domain.Enviroment import PATH_BASE_SINGLE, NORMALIZE, BASEWIDTH
from domain.functions import save, saveByPath

def image(path):
    save(path)

def images(path):
    saveByPath(path)

if __name__ == '__main__':
    print(NORMALIZE)
    image(PATH_BASE_SINGLE)
    #images(PATH_BASE)