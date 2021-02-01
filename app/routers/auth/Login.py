#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Login.py
@Time    :   2021/01/29 19:57:34
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter
from pydantic import BaseModel,EmailStr
from typing import Optional
import hashlib


router = APIRouter()

class UserIn(BaseModel):
    username: str
    userpassword: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def test_save_user(user_in: UserIn):
    print("# 1")
    hashed_password = getMD5_password(user_in.userpassword)
    user_in_db = UserInDB(**user_in.dict(),hashed_password=hashed_password)
    print('User save! But fot test')
    return user_in_db

# 將password加上token之後又用hash加密
def getMD5_password(raw_password: str):
    tokend_password = test_password_plus_token(raw_password)
    md5 = hashlib.md5()
    md5.update(tokend_password.encode('utf-8'))
    res = md5.hexdigest()
    print('hash password is :{}'.format(res))
    return res

# 初步將password加上token -> fbdt加密
def test_password_plus_token(raw_password: str):
    print('raw password is : {}'.format(raw_password))
    tokend_password = 'fbdt'+raw_password
    print('tokend password is: {}'.format(tokend_password))
    return tokend_password

@router.post("/login/",response_model=UserOut)
async def create_uesr(user_in: UserIn):
    user_saved = test_save_user(user_in)
    # user_saved.full_name = 'OK!!'
    return user_saved

