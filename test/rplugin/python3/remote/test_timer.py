# =============================================================================
# FILE: test_timer.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
import asyncio
from unittest.mock import Mock
from remote.timer import Timer

TEST_PAD_TIME = 0.5
TEST_INTVL = 0.01
TEST_ARGS = [1, 2, 3]
TEST_KWARGS = {'arg1': 1, 'arg2': 2}


def TEST_FUNC(*args, **kwargs):
    return None


@pytest.fixture()
def timer(event_loop):
    tmr = Timer(event_loop)
    yield tmr
    tmr.clear()


class TestTimer(object):
    @pytest.mark.asyncio
    async def test_add_handler_timecheck(self, timer):
        expected = 3

        f = Mock(return_value=None)
        id = timer.add_handler(TEST_INTVL, f, TEST_ARGS, TEST_KWARGS)
        await asyncio.sleep(TEST_INTVL * expected + TEST_PAD_TIME)
        actual = f.call_count

        print('ERROR: ' + str(timer.get_handler_exception(id)))
        assert actual == expected

    def test_add_handler_wrapperexception(self, timer):
        assert False

    def test_remove_handler_found(self, timer):
        expected = True

        id = timer.add_handler(TEST_INTVL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = timer.remove_handler(id)

        assert actual == expected

    def test_remove_handler_missing(self, timer):
        expected = False

        id = '12345'
        actual = timer.remove_handler(id)

        assert actual == expected

    def test_get_handler_interval_found(self, timer):
        expected = TEST_INTVL

        id = timer.add_handler(TEST_INTVL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = timer.get_handler_interval(id)

        assert actual == expected

    def test_get_handler_interval_missing(self, timer):
        expected = None

        id = '12345'
        actual = timer.get_handler_interval(id)

        assert actual == expected

    def test_get_handler_function_found(self, timer):
        expected = TEST_FUNC

        id = timer.add_handler(TEST_INTVL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = timer.get_handler_function(id)

        assert actual == expected

    def test_get_handler_function_missing(self, timer):
        expected = None

        id = '12345'
        actual = timer.get_handler_function(id)

        assert actual == expected

    def test_get_handler_args_found(self, timer):
        expected = TEST_ARGS

        id = timer.add_handler(TEST_INTVL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = timer.get_handler_args(id)

        assert actual == expected

    def test_get_handler_args_missing(self, timer):
        expected = None

        id = '12345'
        actual = timer.get_handler_args(id)

        assert actual == expected

    def test_get_handler_kwargs_found(self, timer):
        expected = TEST_KWARGS

        id = timer.add_handler(TEST_INTVL, TEST_FUNC, TEST_ARGS, TEST_KWARGS)
        actual = timer.get_handler_kwargs(id)

        assert actual == expected

    def test_get_handler_kwargs_missing(self, timer):
        expected = None

        id = '12345'
        actual = timer.get_handler_kwargs(id)

        assert actual == expected
