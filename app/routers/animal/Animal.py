#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Animal.py
@Time    :   2021/01/17 21:54:35
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import  APIRouter

router = APIRouter()

@router.get("/animal/",tags=["animal"])
async def read_animal():
    return [{"animal_name":"Catty"},{"animal_name":"John"}]