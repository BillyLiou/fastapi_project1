#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2021/02/14 00:30:33
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

class Config:
    def __init__(self,config_dict:dict):
        self.config_dict = config_dict

app_config = Config({})