"""
log module
"""

import os
import logging
import logging.handlers

from sven.utils.singletone import singleton
from sven.api.exception.path import PathNotFoundError

@singleton
class Log(object):

    def __init__(self, log_path='E:/log'):
        self._init_env(log_path)

    def _init_env(self, log_path):
        try:
            path_exist = os.path.exists(log_path)
            if not path_exist:
                os.mkdir(log_path)

        except OSError:
            raise PathNotFoundError("Paht %s Not Found" %log_path)

        if log_path.endswith('/'):
            error_log = log_path + 'error.log'
            normal_log = log_path + 'access.log'
        else:
            error_log = log_path + '/error.log'
            normal_log = log_path + '/access.log'

        error_handler = logging.handlers.RotatingFileHandler(error_log, maxBytes=1024*1024, backupCount=3)
        error_handler.setLevel(logging.ERROR)

        normal_handler = logging.handlers.RotatingFileHandler(normal_log, maxBytes=1024*1024, backupCount=3)
        normal_handler.setLevel(logging.DEBUG)

        fmt_str = '%(asctime)s %(filename)s:%(lineno)s %(levelname)-8s [-] %(message)s'
        fmt = logging.Formatter(fmt_str)

        normal_filter = NormalFilter()
        error_filter = ErrorFilter()

        error_handler.setFormatter(fmt)
        normal_handler.setFormatter(fmt)

        error_handler.addFilter(error_filter)
        normal_handler.addFilter(normal_filter)

        self.logger = logging.getLogger('sven')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(normal_handler)
        self.logger.addHandler(error_handler)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)


class NormalFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO, logging.WARNING)


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.ERROR, logging.CRITICAL)