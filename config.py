import os

class Config(object):
    RMQ_UNM = ""
    RMQ_PWD = ""
    RMQ_HOST = ""
    RMQ_PORT = 0

_config = Config()
_config.RMQ_UNM = os.environ['RMQ_UNM']
_config.RMQ_PWD = os.environ['RMQ_PWD']
_config.RMQ_HOST = os.environ['RMQ_HOST']
_config.RMQ_PORT = int(os.environ['RMQ_PORT'])


def get_config() -> Config:
    return _config
