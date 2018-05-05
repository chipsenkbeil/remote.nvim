# =============================================================================
# FILE: test_file.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
import pytest
import msgpack
from remote.packet import (
    Content,
    Header,
    Metadata,
    Packet,
)
from remote.messages.constants import (
    MESSAGE_METADATA_CHUNK_INDEX,
    MESSAGE_METADATA_FILE_LENGTH,
    MESSAGE_METADATA_FILE_VERSION,
    MESSAGE_METADATA_TOTAL_CHUNKS,
    MESSAGE_SUBTYPE,
    MESSAGE_SUBTYPE_BROADCAST,
    MESSAGE_SUBTYPE_REQUEST,
    MESSAGE_SUBTYPE_RESPONSE,
    MESSAGE_TYPE_FILE_CHANGED,
    MESSAGE_TYPE_FILE_LIST,
    MESSAGE_TYPE_RETRIEVE_FILE,
    MESSAGE_TYPE_UPDATE_FILE_DATA,
    MESSAGE_TYPE_UPDATE_FILE_START,
)
from remote.messages.file import (
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

TEST_ID = 12345
TEST_USERNAME = 'senkwich'
TEST_SESSION = 'mysession'


###############################################################################
class TestFileListRequestMessage(object):
    _class = FileListRequestMessage
    _path = 'path/to/dir'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            path=self._path,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_FILE_LIST
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_path() == self._path

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            path=self._path,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_FILE_LIST
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_REQUEST)
        assert packet.get_content().get_data() == self._path

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_content(Content().set_data(self._path)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_path() == self._path


###############################################################################
class TestFileListResponseMessage(object):
    _class = FileListResponseMessage
    _file_list = [
        ('path/to/file', 0),
        ('path/to/dir', -1),
        ('path/to/other/file', 7),
    ]

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_list=self._file_list,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_FILE_LIST
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_list() == self._file_list

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_list=self._file_list,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_FILE_LIST
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_RESPONSE)
        assert packet.get_content().get_data() == self._file_list

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_content(Content().set_data(self._file_list)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_list() == self._file_list


###############################################################################
class TestRetrieveFileRequestMessage(object):
    _class = RetrieveFileRequestMessage
    _file_path = 'path/to/file'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_RETRIEVE_FILE
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_RETRIEVE_FILE
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_REQUEST)
        assert packet.get_content().get_data() == self._file_path

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_content(Content().set_data(self._file_path)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path


###############################################################################
class TestRetrieveFileResponseMessage(object):
    _class = RetrieveFileResponseMessage
    _file_length = 999
    _file_version = 7
    _total_chunks = 99
    _chunk_index = 12
    _chunk_data = b'chunk data'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_length=self._file_length,
            file_version=self._file_version,
            total_chunks=self._total_chunks,
            chunk_index=self._chunk_index,
            chunk_data=self._chunk_data,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_RETRIEVE_FILE
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_length() == self._file_length
        assert m.get_file_version() == self._file_version
        assert m.get_total_chunks() == self._total_chunks
        assert m.get_chunk_index() == self._chunk_index
        assert m.get_chunk_data() == self._chunk_data

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_length=self._file_length,
            file_version=self._file_version,
            total_chunks=self._total_chunks,
            chunk_index=self._chunk_index,
            chunk_data=self._chunk_data,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_RETRIEVE_FILE
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_RESPONSE)
        assert self._file_length == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_LENGTH))
        assert self._file_version == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION))
        assert self._total_chunks == (
            packet.get_metadata().get_value(MESSAGE_METADATA_TOTAL_CHUNKS))
        assert self._chunk_index == (
            packet.get_metadata().get_value(MESSAGE_METADATA_CHUNK_INDEX))
        assert packet.get_content().get_data() == self._chunk_data

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_metadata(Metadata()
                                .set_value(MESSAGE_METADATA_FILE_LENGTH,
                                           self._file_length)
                                .set_value(MESSAGE_METADATA_FILE_VERSION,
                                           self._file_version)
                                .set_value(MESSAGE_METADATA_TOTAL_CHUNKS,
                                           self._total_chunks)
                                .set_value(MESSAGE_METADATA_CHUNK_INDEX,
                                           self._chunk_index))
                  .set_content(Content().set_data(self._chunk_data)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_length() == self._file_length
        assert m.get_file_version() == self._file_version
        assert m.get_total_chunks() == self._total_chunks
        assert m.get_chunk_index() == self._chunk_index
        assert m.get_chunk_data() == self._chunk_data


###############################################################################
class TestUpdateFileDataRequestMessage(object):
    _class = UpdateFileDataRequestMessage
    _file_length = 999
    _file_version = 7
    _total_chunks = 99
    _chunk_index = 12
    _chunk_data = b'chunk data'

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_length=self._file_length,
            file_version=self._file_version,
            total_chunks=self._total_chunks,
            chunk_index=self._chunk_index,
            chunk_data=self._chunk_data,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_UPDATE_FILE_DATA
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_length() == self._file_length
        assert m.get_file_version() == self._file_version
        assert m.get_total_chunks() == self._total_chunks
        assert m.get_chunk_index() == self._chunk_index
        assert m.get_chunk_data() == self._chunk_data

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_length=self._file_length,
            file_version=self._file_version,
            total_chunks=self._total_chunks,
            chunk_index=self._chunk_index,
            chunk_data=self._chunk_data,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_UPDATE_FILE_DATA
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_REQUEST)
        assert self._file_length == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_LENGTH))
        assert self._file_version == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION))
        assert self._total_chunks == (
            packet.get_metadata().get_value(MESSAGE_METADATA_TOTAL_CHUNKS))
        assert self._chunk_index == (
            packet.get_metadata().get_value(MESSAGE_METADATA_CHUNK_INDEX))
        assert packet.get_content().get_data() == self._chunk_data

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_metadata(Metadata()
                                .set_value(MESSAGE_METADATA_FILE_LENGTH,
                                           self._file_length)
                                .set_value(MESSAGE_METADATA_FILE_VERSION,
                                           self._file_version)
                                .set_value(MESSAGE_METADATA_TOTAL_CHUNKS,
                                           self._total_chunks)
                                .set_value(MESSAGE_METADATA_CHUNK_INDEX,
                                           self._chunk_index))
                  .set_content(Content().set_data(self._chunk_data)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_length() == self._file_length
        assert m.get_file_version() == self._file_version
        assert m.get_total_chunks() == self._total_chunks
        assert m.get_chunk_index() == self._chunk_index
        assert m.get_chunk_data() == self._chunk_data


###############################################################################
class TestUpdateFileStartRequestMessage(object):
    _class = UpdateFileStartRequestMessage
    _file_path = 'path/to/file'
    _file_version = 7

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
            file_version=self._file_version,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_UPDATE_FILE_START
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path
        assert m.get_file_version() == self._file_version

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
            file_version=self._file_version,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_UPDATE_FILE_START
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_REQUEST)
        assert self._file_version == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION))
        assert packet.get_content().get_data() == self._file_path

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_metadata(Metadata()
                                .set_value(MESSAGE_METADATA_FILE_VERSION,
                                           self._file_version))
                  .set_content(Content().set_data(self._file_path)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path
        assert m.get_file_version() == self._file_version


###############################################################################
class TestUpdateFileStartResponseMessage(object):
    _class = UpdateFileStartResponseMessage
    _file_path = 'path/to/file'
    _file_version = 7

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
            file_version=self._file_version,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_UPDATE_FILE_START
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path
        assert m.get_file_version() == self._file_version

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
            file_version=self._file_version,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_UPDATE_FILE_START
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_RESPONSE)
        assert self._file_version == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION))
        assert packet.get_content().get_data() == self._file_path

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_metadata(Metadata()
                                .set_value(MESSAGE_METADATA_FILE_VERSION,
                                           self._file_version))
                  .set_content(Content().set_data(self._file_path)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path
        assert m.get_file_version() == self._file_version


###############################################################################
class TestUpdateFileDataResponseMessage(object):
    _class = UpdateFileDataResponseMessage
    _file_version = 7
    _total_chunks = 99
    _chunks_received = 50

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_version=self._file_version,
            total_chunks=self._total_chunks,
            chunks_received=self._chunks_received,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_UPDATE_FILE_DATA
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_version() == self._file_version
        assert m.get_total_chunks() == self._total_chunks
        assert m.get_chunks_received() == self._chunks_received

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_version=self._file_version,
            total_chunks=self._total_chunks,
            chunks_received=self._chunks_received,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_UPDATE_FILE_DATA
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_RESPONSE)
        assert self._file_version == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION))
        assert self._total_chunks == (
            packet.get_metadata().get_value(MESSAGE_METADATA_TOTAL_CHUNKS))
        assert packet.get_content().get_data() == self._chunks_received

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_metadata(Metadata()
                                .set_value(MESSAGE_METADATA_FILE_VERSION,
                                           self._file_version)
                                .set_value(MESSAGE_METADATA_TOTAL_CHUNKS,
                                           self._total_chunks))
                  .set_content(Content().set_data(self._chunks_received)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_version() == self._file_version
        assert m.get_total_chunks() == self._total_chunks
        assert m.get_chunks_received() == self._chunks_received


###############################################################################
class TestFileChangeBroadcastMessage(object):
    _class = FileChangeBroadcastMessage
    _file_path = 'path/to/file'
    _file_version = 7
    _file_length = 999

    def test_constructor(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
            file_version=self._file_version,
            file_length=self._file_length,
        )
        assert m.get_id() == TEST_ID
        assert m.get_type() == MESSAGE_TYPE_FILE_CHANGED
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path
        assert m.get_file_version() == self._file_version
        assert m.get_file_length() == self._file_length

    def test_to_packet(self):
        m = self._class(
            id=TEST_ID,
            username=TEST_USERNAME,
            session=TEST_SESSION,
            file_path=self._file_path,
            file_version=self._file_version,
            file_length=self._file_length,
        )
        packet = m.to_packet()

        assert packet.get_header().get_id() == TEST_ID
        assert packet.get_header().get_type() == MESSAGE_TYPE_FILE_CHANGED
        assert packet.get_header().get_username() == TEST_USERNAME
        assert packet.get_header().get_session() == TEST_SESSION
        assert packet.get_metadata().get_value(MESSAGE_SUBTYPE) == (
            MESSAGE_SUBTYPE_BROADCAST)
        assert self._file_version == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION))
        assert self._file_length == (
            packet.get_metadata().get_value(MESSAGE_METADATA_FILE_LENGTH))
        assert packet.get_content().get_data() == self._file_path

    def test_from_packet(self):
        packet = (Packet()
                  .set_header(Header()
                              .set_id(TEST_ID)
                              .set_username(TEST_USERNAME)
                              .set_session(TEST_SESSION))
                  .set_metadata(Metadata()
                                .set_value(MESSAGE_METADATA_FILE_VERSION,
                                           self._file_version)
                                .set_value(MESSAGE_METADATA_FILE_LENGTH,
                                           self._file_length))
                  .set_content(Content().set_data(self._file_path)))
        m = self._class.from_packet(packet)

        assert m.get_id() == TEST_ID
        assert m.get_username() == TEST_USERNAME
        assert m.get_session() == TEST_SESSION
        assert m.get_file_path() == self._file_path
        assert m.get_file_version() == self._file_version
        assert m.get_file_length() == self._file_length
