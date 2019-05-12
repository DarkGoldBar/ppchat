#! /usr/bin/python3
# -*- coding: UTF-8 -*-
import os

CONFIG_TEST = dict(
    user_save = os.path.join(os.path.dirname(__file__), 'test_user_save.pickle'),
    listenip = '0.0.0.0',
    serverip = '127.0.0.1',
    serverport = 10000,
    seperator = '\r\n\r\n',
)

CONFIG_BETA = dict(
    listenip = '0.0.0.0',
    serverip = 'http://119.24.190.165',
    serverport = 6776,
    seperator = '\r\n\r\n',
)