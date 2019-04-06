import logging
import time

from logs.log_record import LogRecord


class Formatter(logging.Formatter):

    def __init__(self, environment):
        self.env = environment

    def format(self, record):
        time_fmt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
        time_str = '%s,%03d' % (time_fmt, record.msecs)

        log_record = LogRecord(self.env, record.name, time_str, record.msg, record.levelname, record.module,
                               record.funcName, record.correlationId)
        return str(log_record)