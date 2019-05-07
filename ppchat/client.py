#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import asyncio
import functools
import logging
import sys
from ppchat.config import CONFIG_TEST as CONFIG

SERVER_ADDRESS = CONFIG['serverip'], CONFIG['serverport']
SEPR = CONFIG['seperator']

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

class EchoClient(asyncio.Protocol):
    future = None
    buffer = None

    def __init__(self, messages, future):
        super().__init__()
        self.messages = messages
        self.log = logging.getLogger('EchoClient')
        self.future = future
        self.buffer = list()

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug('connectiong to {} port {}'.format(*self.address))
        for msg in self.messages:
            transport.write(msg)
            self.log.debug('sending {!r}'.format(msg))

        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)

    def connnection_lost(self, exc):
        self.log.debug('server closed connection')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)
        super().connection_lost(exc)


if __name__ == "__main__":
    log = logging.getLogger('main')

    MESSAGES = [
        b'This is the message. ',
        b'It will be sent ',
        b'in parts.',
    ]

    loop = asyncio.get_event_loop()

    client_completed = asyncio.Future()
    client_factory = functools.partial(EchoClient,messages=MESSAGES,future=client_completed)
    coro = loop.create_connection(client_factory, *SERVER_ADDRESS)

    log.debug('waiting for client to complete')
    try:
        loop.run_until_complete(coro)
        loop.run_until_complete(client_completed)
    finally:
        log.debug('closing event loop')
        loop.close()