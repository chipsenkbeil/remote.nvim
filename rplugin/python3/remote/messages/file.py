# =============================================================================
# FILE: file.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from uuid import uuid4
from . import register
from .base import (
    BaseBroadcastMessage,
    BaseRequestMessage,
    BaseResponseMessage,
)
from .constants import (
    MESSAGE_DEFAULT_CHUNK_DATA,
    MESSAGE_DEFAULT_CHUNK_INDEX,
    MESSAGE_DEFAULT_CHUNKS_RECEIVED,
    MESSAGE_DEFAULT_FILE_LENGTH,
    MESSAGE_DEFAULT_FILE_LIST,
    MESSAGE_DEFAULT_FILE_PATH,
    MESSAGE_DEFAULT_FILE_VERSION,
    MESSAGE_DEFAULT_SESSION,
    MESSAGE_DEFAULT_TOTAL_CHUNKS,
    MESSAGE_DEFAULT_USERNAME,
    MESSAGE_METADATA_CHUNK_INDEX,
    MESSAGE_METADATA_FILE_LENGTH,
    MESSAGE_METADATA_FILE_VERSION,
    MESSAGE_METADATA_TOTAL_CHUNKS,
    MESSAGE_TYPE_FILE_CHANGED,
    MESSAGE_TYPE_FILE_LIST,
    MESSAGE_TYPE_RETRIEVE_FILE,
    MESSAGE_TYPE_UPDATE_FILE_DATA,
    MESSAGE_TYPE_UPDATE_FILE_START,
)


###############################################################################
@register
class FileListRequestMessage(BaseRequestMessage):
    _type = MESSAGE_TYPE_FILE_LIST

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


###############################################################################
@register
class FileListResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_FILE_LIST

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


###############################################################################
@register
class RetrieveFileRequestMessage(BaseRequestMessage):
    _type = MESSAGE_TYPE_RETRIEVE_FILE

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


###############################################################################
@register
class RetrieveFileResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_RETRIEVE_FILE

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


###############################################################################
@register
class UpdateFileStartRequestMessage(BaseRequestMessage):
    _type = MESSAGE_TYPE_UPDATE_FILE_START

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        file_path=MESSAGE_DEFAULT_FILE_PATH,
        file_version=MESSAGE_DEFAULT_FILE_VERSION,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._file_path = file_path
        self._file_version = file_version

    def get_file_path(self):
        """Returns the path to the file relative to vim.

        :returns: The path to the file as a string
        """
        return self._file_path

    def get_file_version(self):
        """Returns the version of the file (base 0).

        :returns: The version of the file as an int
        """
        return self._file_version

    def to_packet(self):
        packet = super().to_packet()
        packet.get_metadata().set_value(
            MESSAGE_METADATA_FILE_VERSION, self._file_version)
        packet.get_content().set_data(self._file_path)
        return packet

    @staticmethod
    def from_packet(packet):
        return UpdateFileStartRequestMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            file_path=packet.get_content().get_data(),
            file_version=packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION),
            parent=None,
        )


###############################################################################
@register
class UpdateFileStartResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_UPDATE_FILE_START

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        file_path=MESSAGE_DEFAULT_FILE_PATH,
        file_version=MESSAGE_DEFAULT_FILE_VERSION,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._file_path = file_path
        self._file_version = file_version

    def get_file_path(self):
        """Returns the path to the file relative to vim.

        :returns: The path to the file as a string
        """
        return self._file_path

    def get_file_version(self):
        """Returns the next version of the file should the data be fully sent
        by the client and received by the server.

        :returns: The version of the file as an int
        """
        return self._file_version

    def to_packet(self):
        packet = super().to_packet()
        packet.get_metadata().set_value(
            MESSAGE_METADATA_FILE_VERSION, self._file_version)
        packet.get_content().set_data(self._file_path)
        return packet

    @staticmethod
    def from_packet(packet):
        return UpdateFileStartResponseMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            file_path=packet.get_content().get_data(),
            file_version=packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION),
            parent=None,
        )


###############################################################################
@register
class UpdateFileDataRequestMessage(BaseRequestMessage):
    _type = MESSAGE_TYPE_UPDATE_FILE_DATA

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
        return UpdateFileDataRequestMessage(
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


###############################################################################
@register
class UpdateFileDataResponseMessage(BaseResponseMessage):
    _type = MESSAGE_TYPE_UPDATE_FILE_DATA

    def __init__(
        self,
        id=str(uuid4()),
        username=MESSAGE_DEFAULT_USERNAME,
        session=MESSAGE_DEFAULT_SESSION,
        file_version=MESSAGE_DEFAULT_FILE_VERSION,
        chunks_received=MESSAGE_DEFAULT_CHUNKS_RECEIVED,
        total_chunks=MESSAGE_DEFAULT_TOTAL_CHUNKS,
        parent=None
    ):
        super().__init__(id, username, session, parent)
        self._file_version = file_version
        self._chunks_received = chunks_received
        self._total_chunks = total_chunks

    def get_file_version(self):
        """Returns the candidate next version of file. If all chunks have
        been received, this version represents the new file version.

        :returns: The version as an integer
        """
        return self._file_version

    def get_chunks_received(self):
        """Returns the total number of chunks that have been received
        thus far.

        :returns: The total number of chunks
        """
        return self._chunks_received

    def get_total_chunks(self):
        """Returns the total number of chunks that are expected.

        :returns: The total number of chunks as an integer
        """
        return self._total_chunks

    def to_packet(self):
        packet = super().to_packet()
        (packet.get_metadata()
         .set_value(MESSAGE_METADATA_FILE_VERSION, self._file_version)
         .set_value(MESSAGE_METADATA_TOTAL_CHUNKS, self._total_chunks))
        packet.get_content().set_data(self._chunks_received)
        return packet

    @staticmethod
    def from_packet(packet):
        return UpdateFileDataResponseMessage(
            id=packet.get_header().get_id(),
            username=packet.get_header().get_username(),
            session=packet.get_header().get_session(),
            file_version=packet.get_metadata().get_value(MESSAGE_METADATA_FILE_VERSION),
            total_chunks=packet.get_metadata().get_value(MESSAGE_METADATA_TOTAL_CHUNKS),
            chunks_received=packet.get_content().get_data(),
            parent=None,
        )


###############################################################################
@register
class FileChangeBroadcastMessage(BaseBroadcastMessage):
    _type = MESSAGE_TYPE_FILE_CHANGED

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
