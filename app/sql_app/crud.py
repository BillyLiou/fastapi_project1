#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   crud.py
@Time    :   2021/01/20 23:50:00
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from sqlalchemy.orm import Session
from . import models

def get_animals(db: Session, animal_id: int):
    return db.query(models.Animal).filter(models.Animal.id == animal_id).first()

