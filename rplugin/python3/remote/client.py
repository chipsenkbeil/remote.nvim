import asyncio
from asyncio import DatagramProtocol


class RemoteClient:
    def __init__(self, addr, port, key=None):
        self.info = {}
        self.info['addr'] = addr
        self.info['port'] = port
        self.info['key'] = key

        self.loop = None
        self.transport = None
        self.protocol = None

    def run(self):
        self.loop = asyncio.get_event_loop()
        listen = self.loop.create_datagram_endpoint(
            RemoteClientProtocol,
            local_addr=(self.info['addr'], self.info['port'])
        )
        transport, protocol = self.loop.run_until_complete(listen)
        self.transport = transport
        self.protocol = protocol

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        self.transport.close()
        self.loop.close()


class RemoteClientProtocol(DatagramProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Established connection to %s' % (transport))

    def connection_lost(self, exc):
        self.transport = None

    def datagram_received(self, data, addr):
        # If no transport, drop the message
        if (self.transport is not None):
            msg = data.decode()
            print('Received %r from %s' % (msg, addr))
