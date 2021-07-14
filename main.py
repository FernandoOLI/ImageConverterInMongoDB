from domain.functions import save, saveByPath, read, clearTmp


def image(path):
    save(path)

def images(path):
    saveByPath(path)

def readImage():
    print("--- %s saveMany ---")
    import time
    start_time = time.time()
    read()
    print("---  Save: %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    #image(PATH_BASE_SINGLE)
    readImage()

