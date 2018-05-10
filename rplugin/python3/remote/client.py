# =============================================================================
# FILE: client.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import asyncio
from asyncio import DatagramProtocol
from uuid import uuid4
from . import logger
from .messages import file, packet_to_message
from .packet import Packet
from .security import new_hmac_from_key


class RemoteClient(logger.LoggingMixin):
    def __init__(self, nvim, addr, port, key=None):
        self.nvim = nvim
        self.is_debug_enabled = True

        self.info = {}
        self.info['addr'] = addr
        self.info['port'] = port
        self.info['key'] = key
        self.info['session'] = uuid4()
        self.info['username'] = 'senkwich'

        self.hmac = new_hmac_from_key(key)
        self.loop = None
        self.transport = None
        self.protocol = None

    def is_running(self):
        return self.transport is not None

    def send(self, data):
        if (not self.is_running()):
            raise Exception('Client is not running or connected!')

        if isinstance(data, str):
            data = data.encode()

        self.transport.sendto(data)
        self.nvim.out_write('Sent "{}"\n'.format(data))

    def start_file_update(self, filename):
        """Starts a new request to the server to update a file.

        :param filename: The full, local path of the file to update
        """
        # TODO: Lookup file version, file length from filename
        r = file.UpdateFileStartRequest(
            username=self.info['username'],
            session=self.info['session'],
            file_path=filename,
            file_version=1.0,
            file_length=0,
        )
        p = r.to_packet().gen_signature(self.client.hmac)
        self.send(p.to_bytes())
        self.nvim.async_call(lambda nvim, filename, addr, port: nvim.out_write(
            'Updating %s on %s:%s' % (filename, addr, port)),
            self.nvim, filename, self.info['addr'], self.info['port'])

    def run(self, cb):
        """Starts the remote client, adding it to the event loop and running
           forever if the loop has not been started elsewhere. If the loop is
           already running, this will only add the datagram endpoint to the
           loop.

        :param cb: The callback to invoke when the client is ready
        """
        self.loop = asyncio.get_event_loop()
        connect = self.loop.create_datagram_endpoint(
            lambda: RemoteClientProtocol(self.nvim, self.hmac),
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
    def __init__(self, nvim, hmac):
        self.nvim = nvim
        self.hmac = hmac
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
                is_valid = packet.is_signature_valid(self.hmac)
                msg = packet_to_message(packet)

                if (is_valid and msg is not None):
                    self.handler.process(msg)
                elif (not is_valid):
                    self.error('Dropping invalid packet: %s\n'.format(packet))
                else:
                    self.error('Dropping unknown packet: %s\n'.format(packet))
            except Exception as ex:
                self.error('Unexpected failure: %s\n'.format(ex))
