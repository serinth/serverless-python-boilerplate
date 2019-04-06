import logging
import uuid
from os import getenv
from sys import stdout

from logs import formatter

level_to_value = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}


def get_log_level():
    log_level_name = getenv('LOG_LEVEL', 'DEBUG')
    return level_to_value.get(log_level_name, logging.DEBUG)


def get_logger(module_name):
    log_level = get_log_level()

    handler = logging.StreamHandler(stdout)
    handler.setLevel(log_level)

    fmt = formatter.Formatter(getenv('STAGE', 'dev'))

    handler.setFormatter(fmt)

    log = logging.getLogger(module_name)

    log.setLevel(log_level)
    log.addHandler(handler)

    log_adapter = logging.LoggerAdapter(log, {'correlationId': str(uuid.uuid4())})

    return log_adapter
