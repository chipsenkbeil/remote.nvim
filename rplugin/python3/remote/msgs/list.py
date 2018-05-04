# =============================================================================
# FILE: list.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.msg import *

# Represents the type of packet
MESSAGE_TYPE = 'LIST'


def new(
    username,
    session,
    path,
    parent_header=Header.empty(),
):
    """Creates a new list packet to execute on the remote nvim instance.

    :param username: The name of the user sending the packet
    :param session: The session associated with the packet
    :param path: The path (relative to nvim) to use as the root of files and
                 directories whose names to retrieve
    :param parent_header: Optional parent header to indicate what led to
                          sending the packet
    :returns: The new packet instance
    """
    assert isinstance(path, str)
    return (Packet()
            .set_header(Header()
                        .set_random_id()
                        .set_username(username)
                        .set_session(session)
                        .set_date_now()
                        .set_type(MESSAGE_TYPE)
                        .set_version(MESSAGE_VERSION))
            .set_parent_header(parent_header)
            .set_metadata(Metadata())
            .set_content(Content().set_data(path)))


def is_match(packet):
    """Checks if the provided packet is a list packet.

    :param packet: The packet to check
    :returns: True if a list packet, otherwise False
    """
    return packet.get_header().get_type() == MESSAGE_TYPE


def get_path(packet):
    """Returns the path of the packet.

    :param packet: The packet to check
    :returns: The path to the directory whose files to list
    """
    return packet.get_content().get_data()
