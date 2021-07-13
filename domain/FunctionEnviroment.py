from decouple import config


def validateEnviroment(name_env):
    name = config(name_env)
    if name == 'local' or name == 'cluster':
        return name
    else:
        raise Exception(
            '----- The name of enviroment is not defined to local or cluster, please verify the .env file -------')


defineEnviroment = validateEnviroment('ENVIROMENT')


def ValidateValueInt(name):
    try:
        return int(config(name))
    except:
        return default(name)


def default(x):
    return {
        'BASEWIDTH': 200,
        'BASEHEIGHT': 100,
        'MIN_HEIGHT': 10,
        'MIN_WIDTH': 10
    }.get(x, 1)


def ValidateValueBool(nameEnv):
    try:
        name = config(nameEnv)
        if name == 'True' or name == 'true' or name == '1':
            return True
        if name == 'False' or name == 'false' or name == '0':
            return False
        else:
            return True
    except:
        return True


def DefineConnection():
    if defineEnviroment == 'local':
        return config('CLIENT_DATABASE_LOCAL')
    if defineEnviroment == 'cluster':
        return CreateConnection()
    else:
        return None


def DefineDatabase():
    if defineEnviroment == 'local':
        return config('DATABASE_LOCAL')
    if defineEnviroment == 'cluster':
        return config('DATABASE_ONLINE')
    else:
        return None


def DefineCollection():
    if defineEnviroment == 'local':
        return config('COLLECTION_LOCAL')
    if defineEnviroment == 'cluster':
        return config('COLLECTION_ONLINE')
    else:
        return None


def DefinePath():
    if defineEnviroment == 'local':
        return config('PATH_BASE_LOCAL')
    if defineEnviroment == 'cluster':
        return config('PATH_BASE_ONLINE')
    else:
        return None


def DefinePathSingle():
    if defineEnviroment == 'local':
        return config('PATH_BASE_SINGLE_LOCAL')
    if defineEnviroment == 'cluster':
        return config('PATH_BASE_SINGLE_ONLINE')
    else:
        return None

def DefineAzure():
    import os
    if config('AZURE_STORAGE_CONNECTION_STRING') == 'not':
        return os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    else:
        return config('AZURE_STORAGE_CONNECTION_STRING')

def CreateConnection():
    return config('CLIENT_DATABASE_ONLINE').replace('<DATABASE_USER>', config('DATABASE_USER')) \
        .replace('<DATABASE_ONLINE>', config('DATABASE_ONLINE')) \
        .replace('<ACCESS>', config('ONLINE_ACCESS'))

def AzureContainer():
    return config('AZURE_CONTAINER')

def TempPath():
    return config('TEMP_PATH')

