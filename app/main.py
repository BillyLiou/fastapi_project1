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

from fastapi import FastAPI, Query, Path, Body, Header, Response, Request, HTTPException,status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import ValidationError,RequestValidationError
from fastapi.encoders import jsonable_encoder

from starlette.exceptions import HTTPException as starletteHTTPException

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
from app.routers.description import description
from app.routers.items import update_item
from app.routers.DI import di_practice

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://127.0.0.1"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Animal.router)
app.include_router(Vehicle.router)
app.include_router(Schema.router)
app.include_router(Cake.router)
app.include_router(Login.router)
app.include_router(Error.router)
app.include_router(description.router)
app.include_router(update_item.router)
app.include_router(di_practice.router)

# 寫入日誌 & 日誌相關格式及檔案名配置
FORMAT = '[%(asctime)s] [%(levelname)s][%(module)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.log")
# logging.basicConfig(level=logging.INFO, format=FORMAT,filename=log_filename, filemode='w')

# 先設訂一個自定義的Exception然後有個 @app.exception_handler去定義返回的字段以及錯誤碼為何


class UvicornException(Exception):
    def __init__(self, name: str):
        self.name = name


# 以下兩個function為一組自定義error如何回傳
@app.exception_handler(UvicornException)
async def uvicron_exception_handler(request: Request, exc: UvicornException):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"{exc.name} is Wrong!! This is message for custom error",
        }
    )

@app.get("/testerror/{name}")
async def get_error_name(name: str):
    if name == 'billy':
        raise UvicornException(name=name)
    return {"test_name": name}


# 以下兩個function為一組自定義starlette如何在某個api實作,同上但寫法上不一樣
@app.exception_handler(starletteHTTPException)
async def handle_validation_error(request: Request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/testerror2/{id}")
async def get_error_name2(id: int):
    if id == 1:
        raise HTTPException(status_code=418,detail={"message":"Oh no your input name will get error 418"})
    return {"test_id": id}


# 以下又是另一組錯誤處理的程式碼範例
# 這邊有一個關鍵,雖然Testerror型別範例是可以篩選出int的,但如果傳遞的值為
# {"title":"topic","size":"5"}
# 以上範例是可以允許的,應該是因為
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request:Request, exc:RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail":exc.errors(),"body":exc.body})
    )
class Testerror(BaseModel):
    title: str
    size: int

@app.post("/testerror3")
async def handle_test_error3(testerror: Testerror):
    """
    這是一個測試是否會被RequestValidationError攔截到的範例api
    """
    return testerror

# 根目錄api訪問

@app.get("/")
async def root():
    # logging.info('Receive root')
    return {"message": "OK網路有通"}


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

#TODO:帶有「;」的入參會把;之後的去除,但希望可以忠實呈現校驗不通過
# 不知道為什麼,regex的機制是「;」後面會直接被移除,後需需要研究看看是不是可以當作有特殊符號所有校驗不通過而不是刪除後面的部分
@app.get("/phone")
async def validate_phone(q: Optional[str] = Query(None, regex="^[0-9\-]+$", alias="qqqBB")):
    print('初始密碼:{}'.format(q))
    res = {}
    p = re.compile('[0-9]{10}')
    m = "".join(re.findall('\d+', str(q)))
    print('這兒,{}'.format(m))
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
def update_item(item_id: int, item: Item, x_api_key: Optional[str] = Header(None), response: Response = None):
    if x_api_key:
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
