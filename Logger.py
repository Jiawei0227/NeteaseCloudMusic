#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
该日志类可以把不同级别的日志输出到不同的日志文件中
'''

import os
import sys
import time
import logging
import inspect

handlers = {logging.DEBUG:"log/LOG-debug.log",
            logging.INFO:"log/LOG-info.log",
            logging.WARNING:"log/LOG-warning.log",
            logging.ERROR:"log/LOG-error.log",
            logging.CRITICAL:"log/LOG-critical.log"}

def createHandlers():
    logLevels = handlers.keys()
    for level in logLevels:
        path = os.path.abspath(handlers[level])
        handlers[level] = logging.FileHandler(path)


#加载模块时创建全局变量
createHandlers()

class Log(object):
    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __init__(self,level=logging.NOTSET):
        self.__loggers = {}
        logLevels = handlers.keys()
        for level in logLevels:
            logger = logging.getLogger(str(level))
            #如果不指定level，获得的handler似乎是同一个handler?
            handler = handlers[level]
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.setLevel(level)
            self.__loggers.update({level:logger})

    def info(self,message):
        self.__loggers[logging.INFO].info(message)

    def error(self,message):
        #message = self.getLogMessage("error",message)
        self.__loggers[logging.ERROR].error(message)

    def warning(self,message):
        #message = self.getLogMessage("warning",message)
        self.__loggers[logging.WARNING].warning(message)


    def debug(self,message):
        #message = self.getLogMessage("debug",message)
        self.__loggers[logging.DEBUG].debug(message)


    def critical(self,message):
        #message = self.getLogMessage("critical",message)
        self.__loggers[logging.CRITICAL].critical(message)

if __name__ == "__main__":
    logger = Log()
    logger.debug("debug")
    logger = Log()
    logger.info("info")
    logger = Log()
    logger.warning("warning")
    logger = Log()
    logger.error("error")
    logger = Log()
    logger.critical("critical")
