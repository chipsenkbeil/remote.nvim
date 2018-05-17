# =============================================================================
# FILE: client.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from .base import BaseHandler


class ClientHandler(BaseHandler):
    def __init__(self, nvim, send):
        """Initializes client actions with with neovim instance to use to
        perform vim-specific operations and a send function to relay responses.

        :param nvim: The neovim instance to use for various operations
        :param send: The function that takes a series of bytes to send to
                     the server
        """
        super(nvim, send)

    def initialize(self):
        """Initializes the registry so it can respond to messages."""
        r = self.registry

