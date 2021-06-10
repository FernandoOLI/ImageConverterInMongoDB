from domain.functions import save, saveByPath

def image(path):
    save(path)

def images(path):
    saveByPath(path)

if __name__ == '__main__':
    #image("image.png")
    images("C:/Users/olive/Pictures/images/")