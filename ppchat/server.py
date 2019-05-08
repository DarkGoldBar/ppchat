#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import asyncio
import logging
import functools
import sys
from ppchat.config import CONFIG_TEST as CONFIG

SERVER_ADDRESS = CONFIG['serverip'], CONFIG['serverport']
SEPR = CONFIG['seperator']

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

class EchoServer(asyncio.Protocol):
    transport = None
    buffer = None
    responser = None
    
    def __init__(self, *arg, **kwargs):
        self.responser = kwargs.pop('responser', echo_responser)
        super().__init__(*arg, **kwargs)

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.buffer = ''
        self.log = logging.getLogger('EchoServer_{}_{}'.format(*self.address))
        self.log.debug('connection accepted')

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))
        self.buffer += data.decode()
        self.check_buffer()

    def eof_received(self):
        self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            self.log.error('ERROR: {}'.format(error))
        else:
            self.log.debug('closing')
        super().connection_lost(error)

    def check_buffer(self, flush=False):
        buffered = self.buffer.split(SEPR)
        self.buffer = ("" if flush else buffered.pop(-1))

        for message in buffered:
            self.log.debug('process buffered message')
            resp = self.responser(message)

            data = resp.encode()
            self.transport.write(data)
            self.log.debug('sent {!r}'.format(data))


def echo_responser(x):
    return x


if __name__ == "__main__":
    def test_responser(x):
        return x.upper()

    log = logging.getLogger('main')
    # Create the server and let the loop finish the coroutine before
    # starting the real event loop.
    loop = asyncio.get_event_loop()
    server_factory = functools.partial(EchoServer, responser=test_responser)
    coro = loop.create_server(server_factory, CONFIG['listenip'], CONFIG['serverport'])
    server = loop.run_until_complete(coro)
    log.debug('starting up on {} port {}'.format(CONFIG['listenip'], CONFIG['serverport']))

    # Enter the event loop permanently to handle all connections.
    try:
        loop.run_forever()
    finally:
        log.debug('closing server')
        server.close()
        loop.run_until_complete(server.wait_closed())
        log.debug('closing event loop')
        loop.close()