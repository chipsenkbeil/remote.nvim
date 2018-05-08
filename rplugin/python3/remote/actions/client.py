# =============================================================================
# FILE: client.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from .base import BaseHandler
from ..messages.command import (
    CommandRequestMessage,
    CommandResponseMessage,
)
from ..messages.error import (
    ErrorBroadcastMessage,
    ErrorResponseMessage,
)
from ..messages.file import (
    FileChangeBroadcastMessage,
    FileListRequestMessage,
    FileListResponseMessage,
    RetrieveFileRequestMessage,
    RetrieveFileResponseMessage,
    UpdateFileDataRequestMessage,
    UpdateFileDataResponseMessage,
    UpdateFileStartRequestMessage,
    UpdateFileStartResponseMessage,
)


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
        r.register(CommandRequestMessage, self._command_request)
        r.register(CommandResponseMessage, self._command_response)
        r.register(ErrorBroadcastMessage, self._error_broadcast)
        r.register(ErrorResponseMessage, self._error_response)
        r.register(FileChangeBroadcastMessage, self._file_change_broadcast)
        r.register(FileListRequestMessage, self._file_list_request)
        r.register(FileListResponseMessage, self._file_list_response)
        r.register(RetrieveFileRequestMessage, self._retrieve_file_request)
        r.register(RetrieveFileResponseMessage, self._retrieve_file_response)
        r.register(UpdateFileDataRequestMessage, self._update_file_data_request)
        r.register(UpdateFileDataResponseMessage, self._update_file_data_response)
        r.register(UpdateFileStartRequestMessage, self._update_file_start_request)
        r.register(UpdateFileStartResponseMessage, self._update_file_start_response)

    def _command_request(self, msg):
        return None

    def _command_response(self, msg):
        return None

    def _error_broadcast(self, msg):
        self.nvim.async_call(lambda nvim, text: nvim.err_write(
            'Error: %s\n' % text), self.nvim, msg.get_error_text())
        return None

    def _error_response(self, msg):
        self.nvim.async_call(lambda nvim, text: nvim.err_write(
            'Error: %s\n' % text), self.nvim, msg.get_error_text())
        return None

    def _file_change_broadcast(self, msg):
        return None

    def _file_list_request(self, msg):
        return None

    def _file_list_response(self, msg):
        return None

    def _retrieve_file_request(self, msg):
        return None

    def _retrieve_file_response(self, msg):
        return None

    def _update_file_start_request(self, msg):
        return None

    def _update_file_start_response(self, msg):
        return None

    def _update_file_data_request(self, msg):
        return None

    def _update_file_data_response(self, msg):
        return None
