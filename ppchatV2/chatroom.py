#! /usr/bin/python3
# -*- coding: UTF-8 -*-
import time

class myMessage():
    def __init__(self, From, To, Text):
        self.From = From
        self.To = To
        self.Text = Text
        self.time_send = time.time()