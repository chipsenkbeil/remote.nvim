# =============================================================================
# FILE: timer.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import asyncio


class Timer(object):
    def __init__(self, loop):
        self._loop = loop

    def add_handler(self, seconds, handler, *args, **kwargs):
        @asyncio.coroutine
        def handler_wrapper():
            yield from asyncio.sleep(seconds)
            handler()
            self.add_handler(seconds, handler)

        self._loop.create_task(handler_wrapper())
