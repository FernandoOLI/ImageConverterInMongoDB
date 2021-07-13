from domain.FunctionEnviroment import ValidateValueInt, ValidateValueBool, DefineConnection, DefineDatabase, \
    DefineCollection, DefinePath, DefinePathSingle, DefineAzure, AzureContainer, TempPath

CLIENT_DATABASE = DefineConnection()
DATABASE = DefineDatabase()
COLLECTION = DefineCollection()
PATH_BASE = DefinePath()
PATH_BASE_SINGLE = DefinePathSingle()
AZURE_CONNECTION = DefineAzure()
AZURE_CONTAINER = AzureContainer()
TEMP_PATH = TempPath()
BASEWIDTH = ValidateValueInt('BASEWIDTH')
BASEHEIGHT = ValidateValueInt('BASEHEIGHT')
MIN_HEIGHT = ValidateValueInt('MIN_HEIGHT')
MIN_WIDTH = ValidateValueInt('MIN_WIDTH')
NORMALIZE = ValidateValueBool('NORMALIZE')
CONTADOR = ValidateValueInt('CONTADOR')
