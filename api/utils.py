from os import getenv, environ


def get_environment_variable(environment_variable_name):
    ''' Returns an environment variable's value or raises an error'''
    key = getenv(environment_variable_name)
    if not key:
        raise LookupError('Please set the {} environment variable'
                          .format(environment_variable_name))
    return key


def set_environment_variable(environment_variable_name):
    environment_variable_value = input('>> Please set the value of the {} environment variable: '.format(environment_variable_name))
    environ[environment_variable_name] = environment_variable_value


def get_or_set_environment_variable(environment_variable_name):
    try:
        return get_environment_variable(environment_variable_name)
    except LookupError:
        set_environment_variable(environment_variable_name)
        return get_environment_variable(environment_variable_name)
