#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   database.py
@Time    :   2021/01/20 23:34:59
@Author  :   Billy Liu
@Version :   1.0
@Contact :   billy@test.mail
@Desc    :   None
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

MYSQL_CONFIG = {
    'server': '',
    'user': 'root',
    'password': 'billy0000',
    'default_db': 'myDB'
}
MYSQL_DATABASE_URL = 'mysql+pymysql://root:billy0000@127.0.0.1:3306/myDB?charset=utf8'

engine = create_engine(MYSQL_DATABASE_URL,pool_pre_ping=True)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()