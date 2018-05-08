# =============================================================================
# FILE: error.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from uuid import uuid4
from .base import (
    BaseBroadcast,
    BaseResponse,
)
from .constants import (
    MESSAGE_DEFAULT_ERROR_TEXT,
    MESSAGE_DEFAULT_SESSION,
    MESSAGE_DEFAULT_USERNAME,
    MESSAGE_TYPE_ERROR,
)


class ErrorResponse(BaseResponse):
    _type = MESSAGE_TYPE_ERROR

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
        return ErrorResponse(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            error_text=packet.get_content().get_data(),
            parent=None,
        )


class ErrorBroadcast(BaseBroadcast):
    _type = MESSAGE_TYPE_ERROR

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
        return ErrorBroadcast(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            error_text=packet.get_content().get_data(),
            parent=None,
        )
