#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Cake.py
@Time    :   2021/01/24 22:57:30
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class Cake(BaseModel):
    name: str
    flavor: str

class cakein(BaseModel):
    name: str
    flavor: str
    amount: int
    quantity: int
    orderName: str

class cakeout(BaseModel):
    name: str
    description: str
    orderName: Optional[str]

@router.post("/cake/", response_model=Cake)
async def base_info(cake: Cake):
    return cake

@router.post("/cake/order",response_model=cakeout,response_model_exclude_unset=True)
async def cakeOrder(cake: cakein):
    return cake
    
@router.post("/cake/order2", response_model=cakeout,response_model_include={"name","description"})
async def cakeOrder2(cake: cakein): 
    if cake.quantity > 10:
        cakeout.description = "訂的數量過多要注意喲"
    else: 
        cakeout.description = "您的商品將在3天以內抵達"
    return {"name":cake.name,"description":cakeout.description}

@router.post("/cake/order3", response_model=cakeout,response_model_exclude_unset=True)
async def ccakeOrder3(cake: cakein):
    res = transformCake(cake)
    return res


def transformCake(cake:cakein) -> cakeout:
    cname = cake.name
    description = ''
    if cake.amount < 500 and cake.quantity < 10:
        description = '您的商品數量:{},總金額:{},將於3日以內送達'.format(cake.quantity, cake.quantity*cake.amount)
        return {"name": cname, "description":description}
    else:
        description = '您的商品數量:{},總金額:{},請親自來店取貨'.format(cake.quantity, str(cake.quantity*cake.amount))
        return {"name": cname, "description":description,"orderName":cake.orderName}