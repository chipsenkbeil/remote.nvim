# =============================================================================
# FILE: error.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from uuid import uuid4
from .base import *
from .constants import *


class ErrorResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_ERROR
    _error_text = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        error_text=MESSAGE_DEFAULT_ERROR_TEXT,
        parent=None,
    ):
        super().__init__(id, username, session, parent)

        if isinstance(error_text, Exception):
            error_text = str(error_text)

        self._error_text = error_text

    def get_error_text(self):
        """Returns the text of the error represented by this error.

        :returns: The text of the error
        """
        return self._error_text

    def to_packet(self):
        packet = super().to_packet()
        packet.get_content().set_data(self._error_text)
        return packet

    @staticmethod
    def from_packet(packet):
        return ErrorResponseMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            error_text=packet.get_content().get_data(),
            parent=None,
        )


class ErrorBroadcastMessage(BaseBroadcastMessage):
    _type = MESSAGE_TYPE_ERROR
    _error_text = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        error_text=MESSAGE_DEFAULT_ERROR_TEXT,
        parent=None,
    ):
        super().__init__(id, username, session, parent)

        if isinstance(error_text, Exception):
            error_text = str(error_text)

        self._error_text = error_text

    def get_error_text(self):
        """Returns the text of the error represented by this error.

        :returns: The text of the error
        """
        return self._error_text

    def to_packet(self):
        packet = super().to_packet()
        packet.get_content().set_data(self._error_text)
        return packet

    @staticmethod
    def from_packet(packet):
        return ErrorBroadcastMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            error_text=packet.get_content().get_data(),
            parent=None,
        )
