# =============================================================================
# FILE: test_init.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
import pytest
from remote.messages import register, registry
from remote.messages.base import BaseMessage
from remote.messages.constants import MESSAGE_SUBTYPE_REQUEST


def test_register_invalid_class():
    with pytest.raises(Exception):
        register(3)


def test_register_valid_class():
    class MyMessage(BaseMessage):
        _type = 'some type'

        @staticmethod
        def is_request():
            return True

        @staticmethod
        def is_response():
            return False

        @staticmethod
        def is_broadcast():
            return False

    assert register(MyMessage) == MyMessage
    assert registry.lookup('some type', MESSAGE_SUBTYPE_REQUEST) == MyMessage
