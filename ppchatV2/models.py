#! /usr/bin/python3
# -*- coding: UTF-8 -*-
import time

from .db_helper import DBUserinfo

class myUser():
    def __init__(self, username):
        self.username = username
        self.is_authenticated = False
        self.is_active = True

    def authorize(self, password):
        query = {"username": self.username}
        response = DBUserinfo.find_one(query)
        if response:
            if response["password"] == password:
                self.is_authenticated = True
                return 200
            return 401
        return 404


class myMessage():
    def __init__(self, From, To, Text):
        self.From = From
        self.To = To
        self.Text = Text
        self.time_send = time.time()