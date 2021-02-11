#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   di_practice.py
@Time    :   2021/02/11 22:32:10
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter, Depends, Response, Request
from app.routers.DI import common_def,common_interface

router = APIRouter()


# 以下為
@router.get("/di_test",tags=["di"])
async def get_di_test(commons: dict = Depends(common_def.common_def_v1)):
    return commons

# 以下為錯誤示範
# @router.post("/di_test_customer",tags=["di"])
# async def get_di_test_customer(common_customer: dict = Depends(common_interface.Customer)):
#     return common_customer

# 想要校驗body的作法就是有一個common_def裡面有個實作common_verify_body去校驗這個body是否滿足這個格式
@router.post("/di_test_customer_body", tags=["di"])
async def get_di_test_customer_verify_body(common_customer: dict = Depends(common_def.common_verify_body)):
    return common_customer

@router.post("/di_test_customer_header",tags=["di"],dependencies=[Depends(common_def.common_verify_header_token),Depends(common_def.common_verify_header_api_key)])
async def get_di_test_customer_verify_header(common_customer: dict = Depends(common_def.common_verify_body),response: Response = None,request: Request = None):
    response.headers["x-api-key"] = request.headers["x-api-key"]
    response.headers["x-token"] = request.headers["x-token"]
    return {"lalala"}