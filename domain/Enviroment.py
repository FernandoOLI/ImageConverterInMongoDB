from decouple import config
# Get environment variables
from domain.FunctionEnviroment import ValidateValueInt, ValidateValueBool

CLIENT_DATABASE = config('CLIENT_DATABASE')
DATABASE = config('DATABASE')
COLLECTION = config('COLLECTION')
PATH_BASE = config('PATH_BASE')
PATH_BASE_SINGLE = config('PATH_BASE_SINGLE')
BASEWIDTH = ValidateValueInt('BASEWIDTH')
BASEHEIGHT = ValidateValueInt('BASEHEIGHT')
MIN_HEIGHT = ValidateValueInt('MIN_HEIGHT')
MIN_WIDTH = ValidateValueInt('MIN_WIDTH')
NORMALIZE = ValidateValueBool('NORMALIZE')


