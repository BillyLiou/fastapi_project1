#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Animal.py
@Time    :   2021/01/17 21:54:35
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''

from fastapi import  APIRouter, Depends
from app.sql_app import crud,models,schemas
from app.sql_app.database import sessionLocal , engine
from sqlalchemy.orm import Session

router = APIRouter()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()

@router.get("/animal/",tags=["animal"])
async def read_animal():
    return [{"animal_name":"Catty"},{"animal_name":"John"}]

@router.get("/animal/{animal_id}",tags=["animal"],response_model=schemas.Animal)
async def read_animal_mysql(animal_id: int,db: Session = Depends(get_db)):
    animal =  crud.get_animals(db,animal_id)
    return animal