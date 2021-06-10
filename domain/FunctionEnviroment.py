from decouple import config

def ValidateValueInt(name):
    try:
        return int(config(name))
    except:
        return f(name)

def f(x):
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
