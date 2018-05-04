# =============================================================================
# FILE: cmd.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.msg import *

# Represents the type of message
MESSAGE_TYPE = 'CMD'

# Represents relevant command metadata
CMD_METADATA_NAME = 'N'
CMD_METADATA_ARGS = 'A'


def new(
    hmac,
    username,
    session,
    name,
    args,
    parent_header=Header.empty(),
):
    """Creates a new command message to execute on the remote nvim instance.

    :param hmac: The HMAC instance to use when generating a signature
    :param username: The name of the user sending the message
    :param session: The session associated with the message
    :param name: The name of the command to invoke on the remote nvim instance
    :param args: The arguments (as a string) to use in the command invocation
    :param parent_header: Optional parent header to indicate what led to
                          sending the message
    :returns: The new message instance
    """
    assert isinstance(name, str)
    assert isinstance(args, str)
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
                          .set_value(CMD_METADATA_NAME, name)
                          .set_value(CMD_METADATA_ARGS, args))
            .set_content(Content.empty()))


def get_name(message):
    """Returns the name of the command of the message.

    :param message: The message to check
    :returns: The name of the command
    """
    return message.get_metadata().get_value(CMD_METADATA_NAME)


def get_args(message):
    """Returns the arguments of the command of the message.

    :param message: The message to check
    :returns: The arguments of the command (as a string)
    """
    return message.get_metadata().get_value(CMD_METADATA_ARGS)
