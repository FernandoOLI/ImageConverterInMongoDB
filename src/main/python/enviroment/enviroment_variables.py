from src.main.python.enviroment.function_enviroment import ValidateValueInt, ValidateValueBool, DefineConnection, \
    DefineDatabase, \
    DefineCollection, DefinePath, DefinePathSingle, DefineAzure, AzureContainer, TempPath, AzureBackup, AzureName, \
    validateEnviroment

ENVIROMENT = validateEnviroment()
CLIENT_DATABASE = DefineConnection()
DATABASE = DefineDatabase()
COLLECTION = DefineCollection()
PATH_BASE = DefinePath()
PATH_BASE_SINGLE = DefinePathSingle()
AZURE_CONNECTION = DefineAzure()
AZURE_CONTAINER = AzureContainer()
AZURE_BACKUP = AzureBackup()
AZURE_NAME = AzureName()
TEMP_PATH = TempPath()
BASEWIDTH = ValidateValueInt('BASEWIDTH')
BASEHEIGHT = ValidateValueInt('BASEHEIGHT')
MIN_HEIGHT = ValidateValueInt('MIN_HEIGHT')
MIN_WIDTH = ValidateValueInt('MIN_WIDTH')
NORMALIZE = ValidateValueBool('NORMALIZE')
CONTADOR = ValidateValueInt('CONTADOR')
