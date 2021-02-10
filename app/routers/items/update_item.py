#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   update_item.py
@Time    :   2021/02/10 00:45:22
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
faka_data = {}


class Item(BaseModel):
    title: str
    amount: Optional[int] = 0
    description: Optional[str] = None


items = {
    "item1": {"title": "item 1", "amount": 100},
    "item2": {"title": "item 2", "amount": 500, "description": "This is a item 2 desc hey hey"},
    "item3": {"title": "item 3", "amount": 150, "description": "la la la"},
}

# 如果想要阿response為null(沒有賦值的欄位)給不返回,則需要加入response_model_exclude_unset=True

# 讀取
@router.get("/get-item/{item_code}", response_model=Item, response_model_exclude_unset=True)
async def get_item_by_id(item_code: str):
    return items[item_code]

# 新增既有的fake_data
@router.put("/update-fake-data/{id}")
async def update_fake_data_by_id(id: int, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    faka_data[id] = json_compatible_item_data
    print(faka_data)
    return json_compatible_item_data


# 更新已經既有的data
@router.put("/update-items/{item_code}")
async def update_items_by_id(item_code: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_code] = update_item_encoded
    return update_item_encoded

# 利用patch方法只更新部分的data
@router.patch("/update-items/{item_code}",response_model=Item)
async def update_itmes_by_id_patch(item_code: str, item: Item):
    stored_item_data = items[item_code]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_code] = jsonable_encoder(updated_item)
    return updated_item