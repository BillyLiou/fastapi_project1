#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2021/01/20 23:01:28
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

class Car(BaseModel):
    name: str 
    description: Optional[str] = None
    price: float

    class Config:
        schema_extra = {
            'example': {
                'name': 'Mercedez',
                'description': 'It\'s a amazing brand',
                'price': 100.55
            } 
        }

@router.put("/schema/{item_id}",tags=["schema"])
async def update_schma_item(item_id: int, car: Car):
    results = {"item_id":item_id,"car":Car}
    return results
