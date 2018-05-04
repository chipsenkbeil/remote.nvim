# =============================================================================
# FILE: sync.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.packet import *

# Represents the type of packet
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
    """Creates a new sync packet to send data.

    :param username: The name of the user sending the packet
    :param session: The session associated with the packet
    :param filename: The full name of the file (including path) to sync
    :param count: The total number of 'sync' packets related to this one
    :param index: The position this packet has in an ordered sync
    :param data: The bytes to send
    :param length: The length of the bytes to send
    :param parent_header: Optional parent header to indicate what led to
                          sending the packet
    :returns: The new packet instance
    """
    assert isinstance(filename, str)
    assert isinstance(count, int) and count >= 1
    assert isinstance(index, int) and index >= 0
    assert isinstance(data, bytes)
    assert isinstance(length, int) and length >= 1
    return (Packet()
            .set_header(Header()
                        .set_random_id()
                        .set_username(username)
                        .set_session(session)
                        .set_date_now()
                        .set_type(MESSAGE_TYPE)
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
    """Creates a new sync packet to receive data.

    :param username: The name of the user sending the packet
    :param session: The session associated with the packet
    :param filename: The full name of the file (including path) to sync
    :param parent_header: Optional parent header to indicate what led to
                          sending the packet
    :returns: The new packet instance
    """
    assert isinstance(filename, str)
    return (Packet()
            .set_header(Header()
                        .set_random_id()
                        .set_username(username)
                        .set_session(session)
                        .set_date_now()
                        .set_type(MESSAGE_TYPE)
                        .set_version(MESSAGE_VERSION))
            .set_parent_header(parent_header)
            .set_metadata(Metadata()
                          .set_value(
                              SYNC_METADATA_DIRECTION,
                              SYNC_METADATA_DIRECTION_RECV)
                          .set_value(SYNC_METADATA_FILENAME, filename))
            .set_content(Content.empty()))


def is_match(packet):
    """Checks if the provided packet is a sync.

    :param packet: The packet to check
    :returns: True if a sync packet, otherwise False
    """
    return packet.get_header().get_type() == MESSAGE_TYPE


def is_direction_send(packet):
    """Checks if the direction of the sync packet is sending data.

    :param packet: The packet to check
    :returns: True if it is, otherwise False
    """
    return (packet
            .get_metadata()
            .get_value(SYNC_METADATA_DIRECTION)
            ) == SYNC_METADATA_DIRECTION_SEND


def is_direction_recv(packet):
    """Checks if the direction of the sync packet is receiving data.

    :param packet: The packet to check
    :returns: True if it is, otherwise False
    """
    return (packet
            .get_metadata()
            .get_value(SYNC_METADATA_DIRECTION)
            ) == SYNC_METADATA_DIRECTION_RECV


def get_chunk_size(packet):
    """Returns the chunk size of the packet.

    :param packet: The packet to check
    :returns: The size of the packet contents
    """
    return packet.get_metadata().get_value(SYNC_METADATA_CHUNK_SIZE)


def get_chunk_count(packet):
    """Returns the chunk count of the packet.

    :param packet: The packet to check
    :returns: The total number of chunks associated with this packet
    """
    return packet.get_metadata().get_value(SYNC_METADATA_CHUNK_COUNT)


def get_chunk_index(packet):
    """Returns the chunk index of the packet.

    :param packet: The packet to check
    :returns: The position of this packet in a group (base 0)
    """
    return packet.get_metadata().get_value(SYNC_METADATA_CHUNK_INDEX)


def get_filename(packet):
    """Returns name of the file associated with the sync packet.

    :param packet: The packet to check
    :returns: The full file name (including path) relative to neovim
    """
    return packet.get_metadata().get_value(SYNC_METADATA_FILENAME)


def get_data(packet):
    """Returns the data held by the sync packet chunk.

    :param packet: The packet to check
    :returns: The data as a collection of bytes
    """
    return packet.get_content().get_data()
