# =============================================================================
# FILE: server.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from .base import BaseHandler
from ..constants import (
    PACKET_TYPE_TELL_HEARTBEAT,
)


class ServerHandler(BaseHandler):
    def __init__(self, nvim, send, broadcast):
        """Initializes server actions with with neovim instance to use to
        perform vim-specific operations and a send function to relay responses.

        :param nvim: The neovim instance to use for various operations
        :param send: The function that takes a series of bytes to send to
                     the client(s); format of send(bytes, address)
        :param broadcast: The function taht takes a series of bytes to send
                          to all clients
        """
        super(nvim, send)
        self.broadcast = broadcast

    def initialize(self):
        """Initializes the registry so it can respond to messages."""
        r = self.registry
        r.register(PACKET_TYPE_TELL_HEARTBEAT, self._heartbeat)

    def _heartbeat(self, packet):
        """Executed when receiving a heartbeat from a client."""
        return None
