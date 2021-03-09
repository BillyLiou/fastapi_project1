# -*- encoding: utf-8 -*-
'''
@File    :   Login.py
@Time    :   2021/01/29 19:57:34
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pandas import pandas as pd

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl='fb-token')

@router.get("/get-token")
async def get_token(token:str = Depends(oauth2)):
    return {'token':token}
