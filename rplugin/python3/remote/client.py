# =============================================================================
# FILE: client.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import asyncio
from asyncio import DatagramProtocol
from remote import logger
from remote.packet import Packet


class RemoteClient(logger.LoggingMixin):
    def __init__(self, nvim, addr, port, key=None):
        self.nvim = nvim
        self.is_debug_enabled = True

        self.info = {}
        self.info['addr'] = addr
        self.info['port'] = port
        self.info['key'] = key

        self.loop = None
        self.transport = None
        self.protocol = None

    def is_running(self):
        return self.transport is not None

    def send(self, data):
        if (not self.is_running()):
            raise Exception('Client is not running or connected!')

        self.transport.sendto(data.encode())
        self.nvim.out_write('Sent "{}"\n'.format(data))

    def run(self, cb):
        """Starts the remote client, adding it to the event loop and running
           forever if the loop has not been started elsewhere. If the loop is
           already running, this will only add the datagram endpoint to the
           loop.

        :param cb: The callback to invoke when the client is ready
        """
        self.loop = asyncio.get_event_loop()
        connect = self.loop.create_datagram_endpoint(
            lambda: RemoteClientProtocol(self.nvim),
            remote_addr=(self.info['addr'], self.info['port'])
        )

        def ready(future):
            transport, protocol = future.result()
            self.transport = transport
            self.protocol = protocol

            err = None
            if (transport is None or protocol is None):
                err = Exception('Failed to connect to {}:{}'
                                .format(self.info['addr'], self.info['port']))
            cb(err)

        self.loop.create_task(connect).add_done_callback(ready)

    def stop(self):
        """Stops the remote client, removing it from the event loop."""
        if (self.transport is not None):
            self.transport.close()
            self.transport = None
        self.protocol = None


class RemoteClientProtocol(DatagramProtocol, logger.LoggingMixin):
    def __init__(self, nvim):
        self.nvim = nvim
        self.is_debug_enabled = True
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.nvim.async_call(lambda nvim, transport: nvim.out_write(
            'Established connection to %s\n' % transport),
            self.nvim, transport)

    def connection_lost(self, exc):
        self.transport = None

    def datagram_received(self, data, addr):
        # If no transport, drop the packet
        if (self.transport is not None):
            packet = None

            try:
                packet = Packet.read(data)
                self.transport.sendto(packet.to_bytes(), addr)
                self.info('New data: %s' % packet)
                self.nvim.async_call(lambda nvim, msg, addr: nvim.out_write(
                    'Received %r from %s\n' % (msg, addr)), self.nvim, packet, addr)
            except Exception as ex:
                self.nvim.async_call(lambda nvim, ex: nvim.err_write(
                    'Exception %s\n' % ex), self.nvim, ex)
