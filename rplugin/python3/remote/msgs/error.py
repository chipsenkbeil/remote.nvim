# =============================================================================
# FILE: error.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.msg import *

# Represents the type of message
MESSAGE_TYPE = 'ERROR'


def new(
    username,
    session,
    exception,
    parent_header=Header.empty(),
):
    """Creates a new error message to be reported on the remote nvim instance.

    :param username: The name of the user sending the message
    :param session: The session associated with the message
    :param exception: The exception to report
    :param parent_header: Optional parent header to indicate what led to
                          sending the message
    :returns: The new message instance
    """
    assert isinstance(exception, Exception)
    return (Message()
            .set_header(Header()
                        .set_random_msg_id()
                        .set_username(username)
                        .set_session(session)
                        .set_date_now()
                        .set_msg_type(MESSAGE_TYPE)
                        .set_version(MESSAGE_VERSION))
            .set_parent_header(parent_header)
            .set_metadata(Metadata())
            .set_content(Content().set_data(str(exception))))


def is_match(message):
    """Checks if the provided message is an error.

    :param message: The message to check
    :returns: True if an error message, otherwise False
    """
    return message.get_header().get_msg_type() == MESSAGE_TYPE


def get_exception_text(message):
    """Returns the text of the error of the message.

    :param message: The message to check
    :returns: The exception as a string
    """
    return message.get_content().get_data()
