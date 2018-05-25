# =============================================================================
# FILE: test_timer.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
import asyncio
from remote.timer import Timer

TEST_INTERVAL = 0.01
TEST_ARGS = [1, 2, 3]
TEST_KWARGS = {'arg1': 1, 'arg2': 2}


def TEST_FUNC(*args, **kwargs):
    return None


@pytest.fixture(scope='module')
def loop():
    event_loop = asyncio.new_event_loop()
    yield event_loop
    event_loop.stop()
    event_loop.close()


class TestTimer(object):
    def test_add_handler_timecheck(self, loop):
        assert False

    def test_add_handler_wrapperexception(self, loop):
        assert False

    def test_remove_handler_found(self, loop):
        expected = True

        tmr = Timer(loop)
        id = tmr.add_handler(TEST_INTERVAL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = tmr.remove_handler(id)

        assert actual == expected

    def test_remove_handler_missing(self, loop):
        expected = False

        tmr = Timer(loop)
        id = '12345'
        actual = tmr.remove_handler(id)

        assert actual == expected

    def test_get_handler_interval_found(self, loop):
        expected = TEST_INTERVAL

        tmr = Timer(loop)
        id = tmr.add_handler(TEST_INTERVAL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = tmr.get_handler_interval(id)

        assert actual == expected

    def test_get_handler_interval_missing(self, loop):
        expected = None

        tmr = Timer(loop)
        id = '12345'
        actual = tmr.get_handler_interval(id)

        assert actual == expected

    def test_get_handler_function_found(self, loop):
        expected = TEST_FUNC

        tmr = Timer(loop)
        id = tmr.add_handler(TEST_INTERVAL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = tmr.get_handler_function(id)

        assert actual == expected

    def test_get_handler_function_missing(self, loop):
        expected = None

        tmr = Timer(loop)
        id = '12345'
        actual = tmr.get_handler_function(id)

        assert actual == expected

    def test_get_handler_args_found(self, loop):
        expected = TEST_ARGS

        tmr = Timer(loop)
        id = tmr.add_handler(TEST_INTERVAL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = tmr.get_handler_args(id)

        assert actual == expected

    def test_get_handler_args_missing(self, loop):
        expected = None

        tmr = Timer(loop)
        id = '12345'
        actual = tmr.get_handler_args(id)

        assert actual == expected

    def test_get_handler_kwargs_found(self, loop):
        expected = TEST_KWARGS

        tmr = Timer(loop)
        id = tmr.add_handler(TEST_INTERVAL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = tmr.get_handler_kwargs(id)

        assert actual == expected

    def test_get_handler_kwargs_missing(self, loop):
        expected = None

        tmr = Timer(loop)
        id = '12345'
        actual = tmr.get_handler_kwargs(id)

        assert actual == expected
