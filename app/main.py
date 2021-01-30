#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2020/12/26 15:14:35
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''
# 啟動app的指令 uvicorn app.main:app --reload

from fastapi import FastAPI, Query, Path, Body,Header,Response
from typing import Optional
from pydantic import BaseModel, Field
import uvicorn
from enum import Enum
import logging
import datetime
import re


from app.Product import Product, Phone
from app.routers.animal import Animal
from app.routers.vehicle import Vehicle
from app.routers.schema_practice import Schema
from app.routers.response_model_practice import Cake
from app.routers.auth import Login
from app.routers.error_practice import Error


app = FastAPI()
app.include_router(Animal.router)
app.include_router(Vehicle.router)
app.include_router(Schema.router)
app.include_router(Cake.router)
app.include_router(Login.router)
app.include_router(Error.router)

# 寫入日誌 & 日誌相關格式及檔案名配置
FORMAT = '[%(asctime)s] [%(levelname)s][%(module)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.log")
# logging.basicConfig(level=logging.INFO, format=FORMAT,filename=log_filename, filemode='w')


@app.get("/")
async def root():
    logging.info('Receive root')
    return {"message": "Hello World"}


# 以下是api請求 轉換Item 物件的範例
# Query parameter

fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


class Item2(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(
        ..., gt=0, description="The price must be greater than zero"
    )
    tax: Optional[float] = None


@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    # 陣列的幾到幾
    # eg. array[0:2],從0開始要有2個內容
    return fake_items_db[skip: skip + limit]


@app.get("/items2")
async def read_items2(q: Optional[str] = Query(None, min_length=5, max_length=20)):
    result = {"items": [{"item_id": 1, "item_name": "Car"},
                        {"item_id": 2, "item_name": "Bicycle"}]}
    if q:
        result.update({"q": q})
    return result


# You should declare it with ... to mark it as required.
@app.get("/items3/{item_id}")
async def read_items3(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query")
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

# use from pydantic import Field


@app.put("/items4/{item_id}")
async def update_item(item_id: int, item: Item2 = Body(..., embed=False)):
    print(item)
    results = {"item_id":  item_id, "item": item}
    return results


@app.get("/phone")
async def validate_phone(q: Optional[str] = Query(None, regex='^[0-9\-]+$', alias="qqqBB")):
    res = {}
    p = re.compile('[0-9]{10}')
    m = "".join(re.findall('\d+', str(q)))
    reg_res = p.match(m)
    if reg_res:
        res.update({"q": q})
    else:
        res.update({"Result": "Not match 10 numbers"})
    # if p.match('^[0-9]{9}$'):
    #     res.update({"description": "regular expression pass"})
    # res.update({"q":q})
    return res


@app.get("/items/{item_id}")
def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    # logging.info("get parameter: {}".format("/items/"+item_id))
    # 第一版的寫法
    # if q:
    #    return {"item_id": item_id,  "q":q}
    # return {"item_id": item_id}
    # eg. http://127.0.0.1:8000/items/5?q=123

    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is a long description"}
        )
    logging.info("Response: {}".format(item))
    return item
    # eg. http://127.0.0.1:8000/items/foo?short=True


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: str, item_id: str, q: Optional[str] = None, short: bool = False):

    # 下面兩個寫法相比較下者更好
    # logging.info("Get request: {}".format("/users/{user_id}/items/{item_id}"))
    logging.info(f"Get request: /users/{user_id}/items/{item_id}")

    item = {"user_id": user_id, "item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    logging.info("Response : {}".format(item))
    return item



# 以此方式在response的header可以呈現當前的值
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item,x_api_key: Optional[str] = Header(None), response:Response = None):
    if  x_api_key:
        response.headers["x-api-key"] = x_api_key
    return {"item_name": item.name, "item_id": item_id}
    # return {"strange_header": x_api_key}


# 以下是api轉換 Enum 的範例
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{modelName}")
async def get_model(modelName: ModelName):
    if modelName == ModelName.alexnet:
        return {"modelName": modelName, "message": "Deep Learning FTW!"}
    elif modelName == "lenet":
        return {"modelName": modelName, "message": "LeCNN all the images"}

    return {"modelName": modelName, "message": "Have some residuals"}


# 以下是檔案路徑的獲取範例
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"read_file": file_path}


# 以下是引用class在另一個檔案的結構
@app.post("/products/")
async def create_item(product: Product):
    product_dict = product.dict()
    if product.tax:
        price_with_tax = product.price + product.tax
        product_dict.update({"price_with_tax": price_with_tax})
    return product_dict



# if __name__ == '__main__':
#     uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
