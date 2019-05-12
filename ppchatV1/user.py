#! /usr/bin/python3
# -*- coding: UTF-8 -*-

from ppchat.config import CONFIG_TEST as CONFIG

UserCollection = {}

class PPuser():
    def __init__(self, uid, sid=None):
        self.uid = uid
        self.sid = sid
        self.status = 0
        self.transport = None
        self.position = None
        self.info = None

    def login(self, password="dummy"):
        if not password:
            return False
        