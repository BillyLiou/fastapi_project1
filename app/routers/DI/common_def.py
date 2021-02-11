#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   common_def.py
@Time    :   2021/02/11 22:29:39
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from typing import Optional
from fastapi import Body, Header, HTTPException
from app.routers.DI import common_interface

async def common_def_v1(q:Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q,"skip": skip, "limit": limit}

async def common_verify_body(customer: common_interface.Customer = Body(...)):
    return customer

async def common_verify_header_token(x_api_key: str = Header(...)):
    if x_api_key != common_interface.CustomHeader.x_api_key.value:
        print("api-key錯囉")
        raise  HTTPException(status_code=401,detail={"err_message":"x-api-key is wrong"})
    return x_api_key

async def common_verify_header_api_key(x_token: str = Header(...)):
    if x_token != common_interface.CustomHeader.x_token.value:
        print("token錯囉")
        raise HTTPException(status_code=401,detail={"err_message":"x-token is wrong"})
    return x_token