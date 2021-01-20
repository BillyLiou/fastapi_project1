#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Vehicle.py
@Time    :   2021/01/19 10:05:36
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter

from typing import Optional, Set, List 
from pydantic import BaseModel, HttpUrl

router = APIRouter()

class Image(BaseModel):
    name: str
    url: HttpUrl

class Vehicle(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tags: Set[str] = set()
    images: Optional[List[Image]] = None

@router.put("/vehicle/{item_id}",tags=["vehicle"])
async def update_vehicle(item_id: int, vehicle: Vehicle):
    results = {"item_id":item_id , "vehicle": vehicle}
    return results