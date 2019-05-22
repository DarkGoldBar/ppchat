#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo

DBClient = pymongo.MongoClient("mongodb://localhost:27017/")

DBDatebase = DBClient["ppchat"]

DBUserinfo = DBDatebase["userinfo"]


