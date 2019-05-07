#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import asyncio
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

class EchoServer(asyncio.Protocol):
    transport = None
    buffer = None
    
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
        self.check_buffer(flush=True)
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
        if SEPR in self.buffer or flush:
            messages = self.buffer.split(SEPR)[0]
            data = messages.encode()
            self.transport.write(data)
            self.log.debug('sent {!r}'.format(data))


if __name__ == "__main__":
    log = logging.getLogger('main')
    # Create the server and let the loop finish the coroutine before
    # starting the real event loop.
    loop = asyncio.get_event_loop()
    coro = loop.create_server(EchoServer, *SERVER_ADDRESS)
    server = loop.run_until_complete(coro)
    log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

    # Enter the event loop permanently to handle all connections.
    try:
        loop.run_forever()
    finally:
        log.debug('closing server')
        server.close()
        loop.run_until_complete(server.wait_closed())
        log.debug('closing event loop')
        loop.close()