# =============================================================================
# FILE: base.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from ..registry import ActionRegistry


class BaseHandler(object):
    def __init__(self, nvim, send):
        """Initializes client actions with with neovim instance to use to
        perform vim-specific operations and a send function to relay responses.

        :param nvim: The neovim instance to use for various operations
        :param send: The function that takes a series of bytes to send to
                     the server
        """
        self.nvim = nvim
        self.send = send
        self.registry = ActionRegistry()

    def process(self, msg):
        """Processes the provided message using the appropriate action.

        :param msg: The message to process
        :returns: The result of processing the message, or None if no action
                  available for the given message
        """
        return self.registry.process(msg)

    def initialize(self):
        """Initializes the internal registry so it can respond to messages."""
        raise NotImplementedError()
