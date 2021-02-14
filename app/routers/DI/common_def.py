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
from fastapi import Body, Header, HTTPException,Depends,Cookie
from app.routers.DI import common_interface

async def common_def_v1(q:Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q,"skip": skip, "limit": limit}

async def common_verify_body(customer: common_interface.Customer = Body(...)):
    return customer

# 依據x-api-key去校驗是否符合x-api-key
async def common_verify_header_token(x_api_key: str = Header(...)):
    if x_api_key != common_interface.CustomHeader.x_api_key.value:
        print("api-key錯囉")
        raise  HTTPException(status_code=401,detail={"err_message":"x-api-key is wrong"})
    return x_api_key

# 依據x-token去校驗是否是符合token
async def common_verify_header_api_key(x_token: str = Header(...)):
    if x_token != common_interface.CustomHeader.x_token.value:
        print("token錯囉")
        raise HTTPException(status_code=401,detail={"err_message":"x-token is wrong"})
    return x_token


# 實作兩個function作為dependency的範例
def query_extractor(q: Optional[str] = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),last_query: Optional[str] = Cookie(None)
):
    if not q:
        print('print cache')
        print(last_query)
        return last_query
    else:
        print('print current')
        return q