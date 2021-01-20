#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Product.py
@Time    :   2021/01/07 21:02:45
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float 
    tax: Optional[float] = None

@dataclass
class Phone(Product):
    name = 'iPhone'
    description: Optional[str] = 'Fashion iPhone'
    price: float 
    tax: Optional[float] = None