# =============================================================================
# FILE: base.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
from uuid import uuid4
from ..packet import (
    Content,
    Header,
    Metadata,
    Packet,
)
from .constants import (
    MESSAGE_API_VERSION,
    MESSAGE_DEFAULT_SESSION,
    MESSAGE_DEFAULT_USERNAME,
    MESSAGE_SUBTYPE,
    MESSAGE_SUBTYPE_BROADCAST,
    MESSAGE_SUBTYPE_REQUEST,
    MESSAGE_SUBTYPE_RESPONSE,
)


class BaseMessage(object):
    """Represents the base message type that all messages extend."""
    _type = None  # To be filled in by subclasses

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        parent=None
    ):
        self._id = id
        self._username = username
        self._session = session
        self._parent = parent

    def get_id(self):
        return self._id

    def get_type(self):
        return self._type

    def get_username(self):
        return self._username

    def get_session(self):
        return self._session

    def get_parent(self):
        return self._parent

    @staticmethod
    def is_request():
        """Indicates if this message represents a request.

        :returns: True if a request, otherwise False
        """
        raise NotImplementedError()

    @staticmethod
    def is_response():
        """Indicates if this message represents a response.

        :returns: True if a response, otherwise False
        """
        raise NotImplementedError()

    @staticmethod
    def is_broadcast():
        """Indicates if this message represents a broadcast.

        :returns: True if a broadcast, otherwise False
        """
        raise NotImplementedError()

    def to_packet(self):
        """Converts the message into a packet to be sent over the network.

        :returns: The packet structure defined by the specific message
        """
        parent_header = Header.empty()
        if (self._parent is not None):
            parent_header = self._parent.to_packet().get_header()

        return (Packet()
                .set_header(Header()
                            .set_id(self._id)
                            .set_username(self._username)
                            .set_session(self._session)
                            .set_date_now()
                            .set_type(self._type)
                            .set_version(MESSAGE_API_VERSION))
                .set_parent_header(parent_header)
                .set_metadata(Metadata.empty())
                .set_content(Content.empty()))

    @staticmethod
    def from_packet(packet):
        """Converts a packet back into a message construct. Should be
        implemented by subclasses.

        :returns: The message instance representing the packet
        """
        raise NotImplementedError()


class BaseRequest(BaseMessage):
    """Represents the base request message that all requests extend."""

    def __init__(self, id, username, session, parent=None):
        super().__init__(id, username, session, parent)

    @staticmethod
    def is_request():
        """Indicates if this message represents a request.

        :returns: True if a request, otherwise False
        """
        return True

    @staticmethod
    def is_response():
        """Indicates if this message represents a response.

        :returns: True if a response, otherwise False
        """
        return False

    @staticmethod
    def is_broadcast():
        """Indicates if this message represents a broadcast.

        :returns: True if a broadcast, otherwise False
        """
        return False

    def to_packet(self):
        """Converts the message into a packet to be sent over the network.

        :returns: The packet structure defined by the specific message
        """
        packet = super().to_packet()
        packet.get_metadata().set_value(
            MESSAGE_SUBTYPE, MESSAGE_SUBTYPE_REQUEST)
        return packet


class BaseResponse(BaseMessage):
    """Represents the base response message that all responses extend."""

    def __init__(self, id, username, session, parent=None):
        super().__init__(id, username, session, parent)

    @staticmethod
    def is_request():
        """Indicates if this message represents a request.

        :returns: True if a request, otherwise False
        """
        return False

    @staticmethod
    def is_response():
        """Indicates if this message represents a response.

        :returns: True if a response, otherwise False
        """
        return True

    @staticmethod
    def is_broadcast():
        """Indicates if this message represents a broadcast.

        :returns: True if a broadcast, otherwise False
        """
        return False

    def to_packet(self):
        """Converts the message into a packet to be sent over the network.

        :returns: The packet structure defined by the specific message
        """
        packet = super().to_packet()
        packet.get_metadata().set_value(
            MESSAGE_SUBTYPE, MESSAGE_SUBTYPE_RESPONSE)
        return packet


class BaseBroadcast(BaseMessage):
    """Represents the base broadcast message that all broadcasts extend."""

    def __init__(self, id, username, session, parent=None):
        super().__init__(id, username, session, parent)

    @staticmethod
    def is_request():
        """Indicates if this message represents a request.

        :returns: True if a request, otherwise False
        """
        return False

    @staticmethod
    def is_response():
        """Indicates if this message represents a response.

        :returns: True if a response, otherwise False
        """
        return False

    @staticmethod
    def is_broadcast():
        """Indicates if this message represents a broadcast.

        :returns: True if a broadcast, otherwise False
        """
        return True

    def to_packet(self):
        """Converts the message into a packet to be sent over the network.

        :returns: The packet structure defined by the specific message
        """
        packet = super().to_packet()
        packet.get_metadata().set_value(
            MESSAGE_SUBTYPE, MESSAGE_SUBTYPE_BROADCAST)
        return packet
