# =============================================================================
# FILE: cmd.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.packet import *

# Represents the type of packet
MESSAGE_TYPE = 'CMD'

# Represents relevant command metadata
CMD_METADATA_NAME = 'N'
CMD_METADATA_ARGS = 'A'


def new(
    username,
    session,
    name,
    args,
    parent_header=Header.empty(),
):
    """Creates a new command packet to execute on the remote nvim instance.

    :param username: The name of the user sending the packet
    :param session: The session associated with the packet
    :param name: The name of the command to invoke on the remote nvim instance
    :param args: The arguments (as a string) to use in the command invocation
    :param parent_header: Optional parent header to indicate what led to
                          sending the packet
    :returns: The new packet instance
    """
    assert isinstance(name, str)
    assert isinstance(args, str)
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
                          .set_value(CMD_METADATA_NAME, name)
                          .set_value(CMD_METADATA_ARGS, args))
            .set_content(Content.empty()))


def is_match(packet):
    """Checks if the provided packet is a command.

    :param packet: The packet to check
    :returns: True if a command packet, otherwise False
    """
    return packet.get_header().get_type() == MESSAGE_TYPE


def get_name(packet):
    """Returns the name of the command of the packet.

    :param packet: The packet to check
    :returns: The name of the command
    """
    return packet.get_metadata().get_value(CMD_METADATA_NAME)


def get_args(packet):
    """Returns the arguments of the command of the packet.

    :param packet: The packet to check
    :returns: The arguments of the command (as a string)
    """
    return packet.get_metadata().get_value(CMD_METADATA_ARGS)
