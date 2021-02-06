#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   description.py
@Time    :   2021/02/06 17:29:43
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional



router = APIRouter()
class Computer(BaseModel):
    name: str
    brand: str
    color: Optional[str]



@router.post(
    "/desc",
    response_model=Computer,
    summary='Create a computer',
    # 這個和下面的function def doc string 擇一有效
    # description="Create a computer with name,brand,color",
    response_description='This response is the same as request',
    tags=['description']
)
async def create_computer(computer: Computer):
    """
    Create an computer with all the information:

    -  **name**: name of this computer
    -  **brand**: brand of this computer
    -  **color**: color of this computer,but it's optional. Not have to type in  
    """
    return computer


@router.get("/desc2",
    response_model=Computer,
    summary='This method has been deprecated',
    tags=['description'],
    deprecated=True)
async def create_computer2():
    return {"message": "This method has been deprecated"}