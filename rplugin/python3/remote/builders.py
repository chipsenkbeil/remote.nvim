# =============================================================================
# FILE: builders.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from . import constants as c
from .packet import (
    Content,
    Header,
    Metadata,
    Packet,
)


def build_header(username, session, type):
    """Builds a new header with the provided information and setting a new
    unique id, the current date, and current version.

    :param username: The username to set in the header
    :param session: The session to set in the header
    :param type: The packet type to set in the header
    :returns: A new header instance
    """
    return (Header()
            .set_random_id()
            .set_username(username)
            .set_session(session)
            .set_date_now()
            .set_type(type)
            .set_version_current())


def build_bare_packet(username, session, type, parent_header=None):
    """Builds a new packet with empty metadata and content.

    :param username: The username to set in the header
    :param session: The session to set in the header
    :param type: The packet type to set in the header
    :param parent_header: If provided, will use as the parent header
                          of the packet
    :returns: A new packet instance
    """
    ph = parent_header if (parent_header is not None) else Header.empty()
    return (Packet()
            .set_parent_header(ph)
            .set_header(build_header(username, session, type))
            .set_metadata(Metadata.empty())
            .set_content(Content().empty()))


def build_tell_heartbeat(username, session):
    """Builds a new heartbeat packet.

    :param username: The username to set in the header
    :param session: The session to set in the header
    :returns: A new packet instance
    """
    return build_bare_packet(username, session, c.PACKET_TYPE_TELL_HEARTBEAT)

