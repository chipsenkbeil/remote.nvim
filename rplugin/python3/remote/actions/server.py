# =============================================================================
# FILE: server.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from .base import BaseHandler
from ..messages.command import (
    CommandRequest,
    CommandResponse,
)
from ..messages.error import (
    ErrorBroadcast,
    ErrorResponse,
)
from ..messages.file import (
    FileChangeBroadcast,
    FileListRequest,
    FileListResponse,
    RetrieveFileRequest,
    RetrieveFileResponse,
    UpdateFileDataRequest,
    UpdateFileDataResponse,
    UpdateFileStartRequest,
    UpdateFileStartResponse,
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
        r.register(CommandRequest, self._command_request)
        r.register(CommandResponse, self._command_response)
        r.register(ErrorBroadcast, self._error_broadcast)
        r.register(ErrorResponse, self._error_response)
        r.register(FileChangeBroadcast, self._file_change_broadcast)
        r.register(FileListRequest, self._file_list_request)
        r.register(FileListResponse, self._file_list_response)
        r.register(RetrieveFileRequest, self._retrieve_file_request)
        r.register(RetrieveFileResponse, self._retrieve_file_response)
        r.register(UpdateFileDataRequest, self._update_file_data_request)
        r.register(UpdateFileDataResponse, self._update_file_data_response)
        r.register(UpdateFileStartRequest, self._update_file_start_request)
        r.register(UpdateFileStartResponse, self._update_file_start_response)

    def _command_request(self, msg):
        return None

    def _command_response(self, msg):
        return None

    def _error_broadcast(self, msg):
        return None

    def _error_response(self, msg):
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
