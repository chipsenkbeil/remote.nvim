# =============================================================================
# FILE: test_timer.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
import asyncio
from unittest.mock import Mock
from remote.timer import Timer

TEST_INTVL = 0.001
TEST_ARGS = [1, 2, 3]
TEST_KWARGS = {'arg1': 1, 'arg2': 2}


@pytest.fixture()
def timer(event_loop):
    tmr = Timer(event_loop, TEST_INTVL)
    yield tmr
    tmr.stop().clear_exceptions()


class TestTimer(object):
    @pytest.mark.asyncio
    async def test_timecheck(self, timer):
        expected = 3

        f = Mock(return_value=None)
        timer.set_handler(f, TEST_ARGS, TEST_KWARGS).start()

        delay = (TEST_INTVL * expected) * 2
        await asyncio.sleep(delay)

        actual = f.call_count
        assert actual == expected

    @pytest.mark.asyncio
    async def test_exceptions(self, timer):
        f = Mock(return_value=None)
        f.side_effect = Exception('Test Failure')
        timer.set_handler(f, TEST_ARGS, TEST_KWARGS)

        assert len(timer.exceptions()) == 0
        timer.start()

        await asyncio.sleep(TEST_INTVL)
        assert len(timer.exceptions()) > 0
        assert timer.exceptions()[0] == f.side_effect

    @pytest.mark.asyncio
    async def test_clear_exceptions(self, timer):
        f = Mock(return_value=None)
        f.side_effect = Exception('Test Failure')
        timer.set_handler(f, TEST_ARGS, TEST_KWARGS).start()

        await asyncio.sleep(TEST_INTVL)
        assert len(timer.exceptions()) > 0

        timer.stop()
        await asyncio.sleep(TEST_INTVL)

        timer.clear_exceptions()
        assert len(timer.exceptions()) == 0

    def test_running_true_after_start(self, timer):
        f = Mock(return_value=None)
        timer.set_handler(f, TEST_ARGS, TEST_KWARGS).start()

        assert timer.running()

    def test_running_false_after_stop(self, timer):
        f = Mock(return_value=None)
        timer.set_handler(f, TEST_ARGS, TEST_KWARGS).start().stop()

        assert not timer.running()

    def test_interval(self, timer):
        assert timer.interval() == TEST_INTVL
