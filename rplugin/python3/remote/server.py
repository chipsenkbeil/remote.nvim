# =============================================================================
# FILE: server.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from asyncio import DatagramProtocol
from . import logger
from .packet import Packet
from .security import new_hmac_from_key
from .messages import packet_to_message
from .actions.server import ServerHandler


class RemoteServer(logger.LoggingMixin):
    def __init__(self, nvim, addr, port, key):
        self.nvim = nvim
        self.loop = nvim.loop
        self.is_debug_enabled = True

        self.info = {}
        self.info['addr'] = addr
        self.info['port'] = port
        self.info['key'] = key

        self.hmac = new_hmac_from_key(key)
        self.transport = None
        self.protocol = None

    def is_running(self):
        return self.transport is not None

    def send(self, data, addr):
        if (not self.is_running()):
            raise Exception('Server is not running or listening!')

        if isinstance(data, str):
            data = data.encode()

        self.transport.sendto(data, addr)

    def run(self, cb):
        """Starts the remote server, adding it to the event loop and running
           forever if the loop has not been started elsewhere. If the loop is
           already running, this will only add the datagram endpoint to the
           loop.

        :param cb: The callback to invoke when the server is ready
        """
        listen = self.loop.create_datagram_endpoint(
            lambda: RemoteServerProtocol(self.nvim, self.hmac),
            local_addr=(self.info['addr'], self.info['port'])
        )

        def ready(future):
            transport, protocol = future.result()
            self.transport = transport
            self.protocol = protocol

            err = None
            if (transport is None or protocol is None):
                err = Exception('Failed to bind to {}:{}'
                                .format(self.info['addr'], self.info['port']))
            cb(err)

        self.loop.create_task(listen).add_done_callback(ready)

    def stop(self):
        """Stops the remote server, removing it from the event loop."""
        if (self.transport is not None):
            self.transport.close()
            self.transport = None
        self.protocol = None


class RemoteServerProtocol(DatagramProtocol, logger.LoggingMixin):
    def __init__(self, nvim, hmac):
        self.nvim = nvim
        self.hmac = hmac
        self.handler = ServerHandler(
            nvim=nvim,
            send=lambda data, addr: self.transport.sendto(data, addr),
            broadcast=lambda data: 
        self.transport = None
        self.is_debug_enabled = True

    def connection_made(self, transport):
        self.transport = transport
        self.nvim.async_call(lambda nvim, transport: nvim.out_write(
            'Established connection to %s\n' % transport
        ), self.nvim, transport)

    def connection_lost(self, exc):
        self.transport = None

    def datagram_received(self, data, addr):
        # If no transport, drop the packet
        if (self.transport is not None):
            packet = None

            try:
                packet = Packet.read(data)
                is_valid = packet.is_signature_valid(self.hmac)
                msg = packet_to_message(packet)

                if (is_valid and msg is not None):

                self.transport.sendto(packet.to_bytes(), addr)
                self.info('New data: %s\nValid: %s' % (msg, is_valid))
                self.nvim.async_call(lambda nvim, msg, addr, valid: nvim.out_write(
                    'Received %r from %s\nValid: %s\n' % (msg, addr, valid)),
                                     self.nvim, msg, addr, is_valid)
            except Exception as ex:
                self.nvim.async_call(lambda nvim, ex: nvim.err_write(
                                     'Exception %s\n' % ex),
                                     self.nvim, ex)
