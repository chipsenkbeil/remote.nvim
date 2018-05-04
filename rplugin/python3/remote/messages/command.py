# =============================================================================
# FILE: command.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from uuid import uuid4
from ..packet import *
from .base import *

# Represents the types of messages request/response/broadcast
MESSAGE_TYPE_COMMAND = 'COMMAND'

# Defaults for non-provided data
MESSAGE_DEFAULT_COMMAND_NAME = '<NAME>'
MESSAGE_DEFAULT_COMMAND_ARGS = '<ARGS>'


class CommandRequestMessage(BaseRequestMessage):
    _type = MESSAGE_TYPE_COMMAND
    _command_name = None
    _command_args = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        command_name=MESSAGE_DEFAULT_COMMAND_NAME,
        command_args=MESSAGE_DEFAULT_COMMAND_ARGS,
        parent=None,
    ):
        super().__init__(id, username, session, parent)
        self._command_name = command_name
        self._command_args = command_args

    def get_command_name(self):
        """Returns the name of the command to be invoked.

        :returns: The name as a string
        """
        return self._command_name

    def get_command_args(self):
        """Returns the arguments of the command to be invoked.

        :returns: The arguments as a string
        """
        return self._command_args

    def to_packet(self):
        packet = super().to_packet()
        packet.get_content().set_data((self._command_name, self._command_args))
        return packet

    @staticmethod
    def from_packet(packet):
        return CommandRequestMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            command_name=packet.get_content().get_data()[0],
            command_args=packet.get_content().get_data()[1],
            parent=None,
        )


class CommandResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_COMMAND
    _command_result = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        command_result=MESSAGE_DEFAULT_COMMAND_NAME,
        parent=None,
    ):
        super().__init__(id, username, session, parent)
        self._command_result = command_result

    def get_command_result(self):
        """Returns the result of the invoked command.

        :returns: The result as a string
        """
        return self._command_result

    def to_packet(self):
        packet = super().to_packet()
        packet.get_content().set_data(self._command_result)
        return packet

    @staticmethod
    def from_packet(packet):
        return CommandResponseMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            command_result=packet.get_content().get_data(),
            parent=None,
        )
