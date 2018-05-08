# =============================================================================
# FILE: test_error.py
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
    MESSAGE_TYPE_ERROR,
    MESSAGE_SUBTYPE,
    MESSAGE_SUBTYPE_BROADCAST,
    MESSAGE_SUBTYPE_RESPONSE,
)
from remote.messages.error import (
    ErrorBroadcast,
    ErrorResponse,
)

TEST_ID = 12345
TEST_USERNAME = 'senkwich'
TEST_SESSION = 'mysession'


###############################################################################
class TestErrorResponse(object):
    _class = ErrorResponse
    _error_text = 'some error'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            error_text=self._error_text,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_ERROR
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_error_text() == self._error_text

    def test_constructor_using_exception(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            error_text=Exception(self._error_text),
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_ERROR
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_error_text() == self._error_text

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            error_text=self._error_text,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_ERROR
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_RESPONSE)
        assert packet.get_content().get_data() == self._error_text

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_content(Content().set_data(self._error_text)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_error_text() == self._error_text


###############################################################################
class TestErrorBroadcast(object):
    _class = ErrorBroadcast
    _error_text = 'some error'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            error_text=self._error_text,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_ERROR
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_error_text() == self._error_text

    def test_constructor_using_exception(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            error_text=Exception(self._error_text),
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_ERROR
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_error_text() == self._error_text

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            error_text=self._error_text,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_ERROR
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_BROADCAST)
        assert packet.get_content().get_data() == self._error_text

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_content(Content().set_data(self._error_text)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_error_text() == self._error_text
