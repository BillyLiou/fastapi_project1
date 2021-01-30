#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Error.py
@Time    :   2021/01/31 01:09:47
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter,HTTPException

router = APIRouter()

list_error = [{
    "ID": 1,
    "user": "Billy"
}]

@router.get("/error/{id}")
async def read_user_handle_error(id: int):
    # 這裏或許可以用pandas的方式去查找欄位是否符合來實作
    for item in list_error:
        if item['ID'] == id:
            return item
    else:
        raise HTTPException(
            status_code=404,
            detail='What you searched ID is not found',
            headers={"X-Error": "There goes custom error message"}
        )