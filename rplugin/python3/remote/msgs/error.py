# =============================================================================
# FILE: error.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.packet import *

# Represents the type of packet
MESSAGE_TYPE = 'ERROR'


def new(
    username,
    session,
    exception,
    parent_header=Header.empty(),
):
    """Creates a new error packet to be reported on the remote nvim instance.

    :param username: The name of the user sending the packet
    :param session: The session associated with the packet
    :param exception: The exception to report
    :param parent_header: Optional parent header to indicate what led to
                          sending the packet
    :returns: The new packet instance
    """
    assert isinstance(exception, Exception)
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
            .set_content(Content().set_data(str(exception))))


def is_match(packet):
    """Checks if the provided packet is an error.

    :param packet: The packet to check
    :returns: True if an error packet, otherwise False
    """
    return packet.get_header().get_type() == MESSAGE_TYPE


def get_exception_text(packet):
    """Returns the text of the error of the packet.

    :param packet: The packet to check
    :returns: The exception as a string
    """
    return packet.get_content().get_data()
