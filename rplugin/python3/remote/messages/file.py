# =============================================================================
# FILE: file.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from uuid import uuid4
from ..packet import *
from .base import *

# Represents the types of messages request/response/broadcast
MESSAGE_TYPE_FILE_LIST = 'FILE_LIST'
MESSAGE_TYPE_RETRIEVE_FILE = 'RETRIEVE_FILE'
MESSAGE_TYPE_UPDATE_FILE = 'UPDATE_FILE'
MESSAGE_TYPE_FILE_CHANGED = 'FILE_CHANGED'

# Common metadata across file information
MESSAGE_METADATA_FILE_VERSION = 'V'

# Represents file retrieval/update metadata
MESSAGE_METADATA_FILE_LENGTH = 'L'
MESSAGE_METADATA_TOTAL_CHUNKS = 'T'
MESSAGE_METADATA_CHUNK_INDEX = 'I'

# Defaults for not-provided data
MESSAGE_DEFAULT_FILE_PATH = ''
MESSAGE_DEFAULT_FILE_LIST = []
MESSAGE_DEFAULT_FILE_LENGTH = -1
MESSAGE_DEFAULT_FILE_VERSION = 0
MESSAGE_DEFAULT_TOTAL_CHUNKS = 1
MESSAGE_DEFAULT_CHUNK_INDEX = 0
MESSAGE_DEFAULT_CHUNK_DATA = b''


class FileListRequestMessage(BaseRequestMessage):
    _type = MESSAGE_TYPE_FILE_LIST
    _path = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        path=MESSAGE_DEFAULT_FILE_PATH,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._path = path

    def get_path(self):
        return self._path

    def to_packet(self):
        packet = super().to_packet()
        packet.get_content().set_data(self._path)
        return packet

    @staticmethod
    def from_packet(packet):
        return FileListRequestMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            path=packet.get_content().get_data(),
            parent=None,
        )


class FileListResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_FILE_LIST
    _file_list = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        file_list=MESSAGE_DEFAULT_FILE_LIST,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._file_list = file_list

    def get_file_list(self):
        """Returns list of files/directories in the form of
        (name,version) where version is a positive integer
        for a file and -1 if a directory.

        :returns: List of tuples about files/directories
        """
        return self._file_list

    def to_packet(self):
        packet = super().to_packet()
        packet.get_content().set_data(self._file_list)
        return packet

    @staticmethod
    def from_packet(packet):
        return FileListResponseMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            file_list=packet.get_content().get_data(),
            parent=None,
        )


class RetrieveFileRequestMessage(BaseRequestMessage):
    _type = MESSAGE_TYPE_RETRIEVE_FILE
    _file_path = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        file_path=MESSAGE_DEFAULT_FILE_PATH,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._file_path = file_path

    def get_file_path(self):
        """Returns the path to the file relative to vim.

        :returns: The path to the file as a string
        """
        return self._file_path

    def to_packet(self):
        packet = super().to_packet()
        packet.get_content().set_data(self._file_path)
        return packet

    @staticmethod
    def from_packet(packet):
        return RetrieveFileRequestMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            file_path=packet.get_content().get_data(),
            parent=None,
        )


class RetrieveFileResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_RETRIEVE_FILE
    _file_length = None
    _file_version = None
    _total_chunks = None
    _chunk_index = None
    _chunk_data = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        file_length=MESSAGE_DEFAULT_FILE_LENGTH,
        file_version=MESSAGE_DEFAULT_FILE_VERSION,
        total_chunks=MESSAGE_DEFAULT_TOTAL_CHUNKS,
        chunk_index=MESSAGE_DEFAULT_CHUNK_INDEX,
        chunk_data=MESSAGE_DEFAULT_CHUNK_DATA,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._file_length = file_length
        self._file_version = file_version
        self._total_chunks = total_chunks
        self._chunk_index = chunk_index
        self._chunk_data = chunk_data

    def get_file_length(self):
        """Returns the total length of the file (not just this chunk).

        :returns: The total length of the file
        """
        return self._file_length

    def get_file_version(self):
        """Returns the version of the file (base 0).

        :returns: The version of the file as an int
        """
        return self._file_version

    def get_total_chunks(self):
        """Returns the total number of chunks that are being sent for the file.

        :returns: The total number of chunks as an integer
        """
        return self._total_chunks

    def get_chunk_index(self):
        """Returns the position of this chunk (base 0) within the file.

        :returns: The position of this chunk as an integer (base 0)
        """
        return self._chunk_index

    def get_chunk_data(self):
        """Returns the chunk of data representing part/all of the file.

        :returns: The chunk of data as bytes
        """
        return self._chunk_data

    def to_packet(self):
        packet = super().to_packet()
        (packet.get_metadata()
         .set_value(MESSAGE_METADATA_CHUNK_INDEX, self._chunk_index)
         .set_value(MESSAGE_METADATA_TOTAL_CHUNKS, self._total_chunks)
         .set_value(MESSAGE_METADATA_FILE_VERSION, self._file_version)
         .set_value(MESSAGE_METADATA_FILE_LENGTH, self._file_length))
        packet.get_content().set_data(self._chunk_data)
        return packet

    @staticmethod
    def from_packet(packet):
        return RetrieveFileResponseMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            file_length=packet.get_metadata().get_value(MESSAGE_METADATA_FILE_LENGTH),
            file_version=packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION),
            chunk_index=packet.get_metadata().get_value(MESSAGE_METADATA_CHUNK_INDEX),
            total_chunks=packet.get_metadata().get_value(MESSAGE_METADATA_TOTAL_CHUNKS),
            chunk_data=packet.get_content().get_data(),
            parent=None,
        )


class FileChangeBroadcastMessage(BaseBroadcastMessage):
    _type = MESSAGE_TYPE_FILE_CHANGED
    _file_path = None
    _file_version = None
    _file_length = None

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        file_path=MESSAGE_DEFAULT_FILE_PATH,
        file_version=MESSAGE_DEFAULT_FILE_VERSION,
        file_length=MESSAGE_DEFAULT_FILE_LENGTH,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._file_path = file_path
        self._file_version = file_version
        self._file_length = file_length

    def get_file_path(self):
        """Returns the path to the file that changed.

        :returns: The path as a string
        """
        return self._file_path

    def get_file_version(self):
        """Returns the version of the file that changed.

        :returns: The version as an integer
        """
        return self._file_version

    def get_file_length(self):
        """Returns the length of the file that changed.

        :returns: The length as an integer
        """
        return self._file_length

    def to_packet(self):
        packet = super().to_packet()
        (packet.get_metadata()
         .set_value(MESSAGE_METADATA_FILE_VERSION, self._file_version)
         .set_value(MESSAGE_METADATA_FILE_LENGTH, self._file_length))
        packet.get_content().set_data(self._file_path)
        return packet

    @staticmethod
    def from_packet(packet):
        return FileChangeBroadcastMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            file_path=packet.get_content().get_data(),
            file_version=packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION),
            file_length=packet.get_metadata().get_value(MESSAGE_METADATA_FILE_LENGTH),
            parent=None,
        )
