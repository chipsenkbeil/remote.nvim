# =============================================================================
# FILE: test_timer.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
import asyncio
from remote.timer import Timer


@pytest.fixture(scope='module')
def loop():
    event_loop = asyncio.new_event_loop()
    yield event_loop
    event_loop.stop()
    event_loop.close()


class TestTimer(object):
    def test_add_handler_timecheck(self, loop):
        assert False

    def test_remove_handler_found(self, loop):
        assert False

    def test_remove_handler_missing(self, loop):
        assert False

    def test_get_handler_interval_found(self, loop):
        assert False

    def test_get_handler_interval_missing(self, loop):
        assert False

    def test_get_handler_function_found(self, loop):
        assert False

    def test_get_handler_function_missing(self, loop):
        assert False

    def test_get_handler_args_found(self, loop):
        assert False

    def test_get_handler_args_missing(self, loop):
        assert False

    def test_get_handler_kwargs_found(self, loop):
        assert False

    def test_get_handler_kwargs_missing(self, loop):
        tmr = Timer(loop)
        assert False
