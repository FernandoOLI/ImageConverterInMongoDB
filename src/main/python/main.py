from src.main.python.azure_functions.function import clear_backup
from src.main.python.azure_functions.main import run_image


def run():
    print("------------------------ Init ------------------------")
    import time
    start_time = time.time()
    run_image()
    print("---  Save duration: %s seconds ---" % (time.time() - start_time))
    print("------------------------ End ------------------------")

def clear():
    clear_backup()

if __name__ == '__main__':
    run()

