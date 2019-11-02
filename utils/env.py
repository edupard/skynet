import os


def get_env_variable(name):
    value = 'N/A' if name not in os.environ else os.environ[name]
    return '%s=%s;' % (name, value)


def get_env_variables(vars):
    result = ''
    for var in vars:
        result += get_env_variable(var)
    return result
