#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   schema.py
@Time    :   2021/01/22 17:28:17
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from typing import Optional
from pydantic import BaseModel

class AnimalBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
        

class Animal(AnimalBase):
    id: int
    name: str
    height: str
    weight: str
    classification: int
    class Config:
        orm_mode=True
