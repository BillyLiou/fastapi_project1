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
from app.routers.DI import common_def, common_interface
from app.config import app_config

router = APIRouter()


# 以下為這個模塊的初始prefix
@router.get("/")
async def get_di_test(commons: dict = Depends(common_def.common_def_v1)):
    return commons

# 以下為錯誤示範
# @router.post("/di_test_customer",tags=["di"])
# async def get_di_test_customer(common_customer: dict = Depends(common_interface.Customer)):
#     return common_customer

# 想要校驗body的作法就是有一個common_def裡面有個實作common_verify_body去校驗這個body是否滿足這個格式


@router.post("/di_test_customer_body")
async def get_di_test_customer_verify_body(common_customer: dict = Depends(common_def.common_verify_body)):
    return common_customer

# 這個作法可以統一校驗header是不是滿足token和x-api-key是否滿足給定到特定值


@router.post("/di_test_customer_header", dependencies=[Depends(common_def.common_verify_header_token), Depends(common_def.common_verify_header_api_key)])
async def get_di_test_customer_verify_header(common_customer: dict = Depends(common_def.common_verify_body), response: Response = None, request: Request = None):
    response.headers["x-api-key"] = request.headers["x-api-key"]
    response.headers["x-token"] = request.headers["x-token"]
    return {"lalala"}

# 引用配置作為返回


@router.get("/di_test_get_config")
async def get_di_test_config_example():
    # print(app_config.config_dict)
    return {"author": app_config.config_dict['author'], "title": app_config.config_dict['title'], "owner_name": app_config.config_dict['owner']['name'],"owner_dev":app_config.config_dict['owner']['dev']}
