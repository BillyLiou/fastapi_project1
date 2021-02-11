#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   common_interface.py
@Time    :   2021/02/11 23:19:43
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import Query
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class Customer(BaseModel):
    name: str
    phone: Optional[str] = Query(None,regex='^\d{10}$')

class CustomHeader(Enum):
    x_token = 'test-token'
    x_api_key = 'api-key'