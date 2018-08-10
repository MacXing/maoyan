# -*- coding: utf-8 -*- 
# @Time : 2018/8/10 10:06 
# @Author : Allen 
# @Site :  log日志
import logging


class LOG:
    def __init__(self):
        self.logger = logging.getLogger()
        self.LOG_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.file_handel = logging.FileHandler('maoyan.log', encoding='utf8')
        self.file_handel.setFormatter(self.LOG_FORMAT)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handel)

    def get_logger(self):
        return self.logger
