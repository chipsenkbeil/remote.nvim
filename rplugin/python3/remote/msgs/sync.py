# =============================================================================
# FILE: sync.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.msg import *

# Represents the type of message
MESSAGE_TYPE = 'SYNC'

# Represent relevant sync metadata
SYNC_METADATA_DIRECTION = 'D'
SYNC_METADATA_CHUNK_COUNT = 'C'
SYNC_METADATA_CHUNK_INDEX = 'I'
SYNC_METADATA_CHUNK_SIZE = 'S'
SYNC_METADATA_FILENAME = 'F'

SYNC_METADATA_DIRECTION_SEND = 'S'
SYNC_METADATA_DIRECTION_RECV = 'R'


def new_send(
    username,
    session,
    filename,
    count,
    index,
    data,
    length,
    parent_header=Header.empty(),
):
    """Creates a new sync message to send data.

    :param username: The name of the user sending the message
    :param session: The session associated with the message
    :param filename: The full name of the file (including path) to sync
    :param count: The total number of 'sync' messages related to this one
    :param index: The position this message has in an ordered sync
    :param data: The bytes to send
    :param length: The length of the bytes to send
    :param parent_header: Optional parent header to indicate what led to
                          sending the message
    :returns: The new message instance
    """
    assert isinstance(filename, str)
    assert isinstance(count, int) and count >= 1
    assert isinstance(index, int) and index >= 0
    assert isinstance(data, bytes)
    assert isinstance(length, int) and length >= 1
    return (Message()
            .set_header(Header()
                        .set_random_msg_id()
                        .set_username(username)
                        .set_session(session)
                        .set_date_now()
                        .set_msg_type(MESSAGE_TYPE)
                        .set_version(MESSAGE_VERSION))
            .set_parent_header(parent_header)
            .set_metadata(Metadata()
                          .set_value(
                              SYNC_METADATA_DIRECTION,
                              SYNC_METADATA_DIRECTION_SEND)
                          .set_value(SYNC_METADATA_CHUNK_COUNT, count)
                          .set_value(SYNC_METADATA_CHUNK_INDEX, index)
                          .set_value(SYNC_METADATA_CHUNK_SIZE, length)
                          .set_value(SYNC_METADATA_FILENAME, filename))
            .set_content(Content().set_data(data[0:length])))


def new_recv(
    username,
    session,
    filename,
    parent_header=Header.empty(),
):
    """Creates a new sync message to receive data.

    :param username: The name of the user sending the message
    :param session: The session associated with the message
    :param filename: The full name of the file (including path) to sync
    :param parent_header: Optional parent header to indicate what led to
                          sending the message
    :returns: The new message instance
    """
    assert isinstance(filename, str)
    return (Message()
            .set_header(Header()
                        .set_random_msg_id()
                        .set_username(username)
                        .set_session(session)
                        .set_date_now()
                        .set_msg_type(MESSAGE_TYPE)
                        .set_version(MESSAGE_VERSION))
            .set_parent_header(parent_header)
            .set_metadata(Metadata()
                          .set_value(
                              SYNC_METADATA_DIRECTION,
                              SYNC_METADATA_DIRECTION_RECV)
                          .set_value(SYNC_METADATA_FILENAME, filename))
            .set_content(Content.empty()))


def is_match(message):
    """Checks if the provided message is a sync.

    :param message: The message to check
    :returns: True if a sync message, otherwise False
    """
    return message.get_header().get_msg_type() == MESSAGE_TYPE


def is_direction_send(message):
    """Checks if the direction of the sync message is sending data.

    :param message: The message to check
    :returns: True if it is, otherwise False
    """
    return (message
            .get_metadata()
            .get_value(SYNC_METADATA_DIRECTION)
            ) == SYNC_METADATA_DIRECTION_SEND


def is_direction_recv(message):
    """Checks if the direction of the sync message is receiving data.

    :param message: The message to check
    :returns: True if it is, otherwise False
    """
    return (message
            .get_metadata()
            .get_value(SYNC_METADATA_DIRECTION)
            ) == SYNC_METADATA_DIRECTION_RECV


def get_chunk_size(message):
    """Returns the chunk size of the message.

    :param message: The message to check
    :returns: The size of the message contents
    """
    return message.get_metadata().get_value(SYNC_METADATA_CHUNK_SIZE)


def get_chunk_count(message):
    """Returns the chunk count of the message.

    :param message: The message to check
    :returns: The total number of chunks associated with this message
    """
    return message.get_metadata().get_value(SYNC_METADATA_CHUNK_COUNT)


def get_chunk_index(message):
    """Returns the chunk index of the message.

    :param message: The message to check
    :returns: The position of this message in a group (base 0)
    """
    return message.get_metadata().get_value(SYNC_METADATA_CHUNK_INDEX)


def get_filename(message):
    """Returns name of the file associated with the sync message.

    :param message: The message to check
    :returns: The full file name (including path) relative to neovim
    """
    return message.get_metadata().get_value(SYNC_METADATA_FILENAME)


def get_data(message):
    """Returns the data held by the sync message chunk.

    :param message: The message to check
    :returns: The data as a collection of bytes
    """
    return message.get_content().get_data()
