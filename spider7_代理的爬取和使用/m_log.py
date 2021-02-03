import logging
from logging import handlers
import os
import functools

cur_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(cur_path)


class Logger(object):
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def __init__(self, filename=os.path.join(parent_path, "spider7_代理的爬取和使用/LogFiles/spider7_log.log"), level="error", when="D",
                 backupCount=10, interval=1,
                 fmt="%(asctime)s - line:%(lineno)d - [%(levelname)s]: %(message)s"):
        format_str = logging.Formatter(fmt)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(format_str)
        fileHandler = handlers.TimedRotatingFileHandler(filename=filename, when=when, interval=1,
                                                        backupCount=backupCount, encoding="utf-8")
        fileHandler.setFormatter(format_str)
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(self.level_relations.get(level))
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)


def log_exception(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        logger = Logger().logger
        try:
            logger.info("{}({},{})".format(fn.__name__, args, kwargs))
            res = fn(*args, **kwargs)
            return res
        except Exception as e:
            logger.error("{}({},{}) [error]:{}".format(fn.__name__, args, kwargs, e))
            raise
        finally:
            logging.shutdown()
    return wrapper
