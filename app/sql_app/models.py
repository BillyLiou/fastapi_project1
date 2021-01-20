#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2021/01/20 23:42:01
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer,primary_key=True, index=True)
    name =  Column(String)
    height = Column(String)
    weight = Column(String)
    classification = Column(String)