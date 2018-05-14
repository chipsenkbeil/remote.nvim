# =============================================================================
# FILE: test_registry.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
from remote.packet import (
    Content,
    Header,
    Packet,
)
from remote.registry import (
    ActionRegistry,
)

TEST_TYPE = 'some type'


class TestActionRegistry(object):
    def test_register(self):
        def my_action(a):
            return a

        ar = ActionRegistry()
        ar.register(TEST_TYPE, my_action)

        assert ar.lookup(TEST_TYPE) == my_action

    def test_process(self):
        def my_action(p):
            old_value = p.get_content().get_data()
            p.get_content().set_data(1000)
            return old_value

        ar = ActionRegistry()
        ar.register(TEST_TYPE, my_action)

        p = (Packet()
             .set_header(Header()
                         .set_type(TEST_TYPE))
             .set_content(Content()
                          .set_data(999)))

        assert ar.process(p) == 999
        assert p.get_content().get_data() == 1000
