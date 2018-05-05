# =============================================================================
# FILE: test_registry.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
import pytest
from remote.registry import *
from remote.messages.constants import *

TEST_TYPE = 'some type'


class TestMessageRegistry(object):
    def test_register_request(self):
        class M():
            _type = TEST_TYPE

            @staticmethod
            def is_request():
                return True

            @staticmethod
            def is_response():
                return False

            @staticmethod
            def is_broadcast():
                return False

        mr = MessageRegistry()
        mr.register(M)

        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_REQUEST) == M
        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_RESPONSE) is None
        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_BROADCAST) is None

    def test_register_response(self):
        class M():
            _type = TEST_TYPE

            @staticmethod
            def is_request():
                return False

            @staticmethod
            def is_response():
                return True

            @staticmethod
            def is_broadcast():
                return False

        mr = MessageRegistry()
        mr.register(M)

        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_REQUEST) is None
        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_RESPONSE) == M
        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_BROADCAST) is None

    def test_register_broadcast(self):
        class M():
            _type = TEST_TYPE

            @staticmethod
            def is_request():
                return False

            @staticmethod
            def is_response():
                return False

            @staticmethod
            def is_broadcast():
                return True

        mr = MessageRegistry()
        mr.register(M)

        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_REQUEST) is None
        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_RESPONSE) is None
        assert mr.lookup(TEST_TYPE, MESSAGE_SUBTYPE_BROADCAST) == M


class TestActionRegistry(object):
    def test_register(self):
        class A(object):
            _fish = 999

        def my_action(a):
            return a

        ar = ActionRegistry()
        ar.register(A, my_action)

        assert ar.lookup(A()) == my_action

    def test_process(self):
        class A(object):
            def __init__(self):
                self.value = 999

        a_instance = A()

        def my_action(a):
            old_value = a.value
            a.value = 1000
            return old_value

        ar = ActionRegistry()
        ar.register(A, my_action)

        assert ar.process(a_instance) == 999
        assert a_instance.value == 1000
