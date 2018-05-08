# =============================================================================
# FILE: test_command.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
import pytest
import msgpack
from remote.packet import (
    Content,
    Header,
    Packet,
)
from remote.messages.constants import (
    MESSAGE_TYPE_COMMAND,
    MESSAGE_SUBTYPE,
    MESSAGE_SUBTYPE_REQUEST,
    MESSAGE_SUBTYPE_RESPONSE,
)
from remote.messages.command import (
    CommandRequest,
    CommandResponse,
)

TEST_ID = 12345
TEST_USERNAME = 'senkwich'
TEST_SESSION = 'mysession'


###############################################################################
class TestCommandRequest(object):
    _class = CommandRequest
    _command_name = 'CommandName'
    _command_args = 'some args'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            command_name=self._command_name,
            command_args=self._command_args,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_COMMAND
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_command_name() == self._command_name
        assert m.get_command_args() == self._command_args

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            command_name=self._command_name,
            command_args=self._command_args,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_COMMAND
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_REQUEST)
        assert packet.get_content().get_data() == (
            self._command_name, self._command_args)

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_content(Content().set_data(
                      (self._command_name, self._command_args))))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_command_name() == self._command_name
        assert m.get_command_args() == self._command_args


###############################################################################
class TestCommandResponse(object):
    _class = CommandResponse
    _command_result = 'some result'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            command_result=self._command_result,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_COMMAND
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_command_result() == self._command_result

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            command_result=self._command_result,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_COMMAND
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_RESPONSE)
        assert packet.get_content().get_data() == self._command_result

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_content(Content().set_data(self._command_result)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_command_result() == self._command_result
