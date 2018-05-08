# =============================================================================
# FILE: test_module.py (for __init__.py)
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote import messages as msg
from remote.messages import packet_to_message
from remote.packet import (
    Content,
    Header,
    Metadata,
    Packet,
)


def test_packet_to_message_error_broadcast_type():
    assert True == False


def test_packet_to_message_command_response_type():
    assert True == False


def test_packet_to_message_file_request_type():
    assert True == False


def test_packet_to_message_no_match():
    assert True == False
