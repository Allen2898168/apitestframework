import logging
import os
import re
from logging import handlers

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
LoggingMap = {
    "CRITICAL": CRITICAL,
    "FATAL": CRITICAL,
    "ERROR": ERROR,
    "WARNING": WARNING,
    "WARN": WARN,
    "INFO": INFO,
    "DEBUG": DEBUG
}


def system_logging(loglevel, filename, when="M", ):
    logger = logging.getLogger()
    logger.setLevel(LoggingMap[loglevel])
    format_str = logging.Formatter('[%(asctime)s] %(filename)s_%(lineno)d: %(levelname)s:  %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(format_str)
    th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=2, interval=2, encoding='utf-8')
    th.setFormatter(format_str)
    logger.addHandler(sh)
    logger.addHandler(th)


