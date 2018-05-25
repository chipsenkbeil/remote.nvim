# =============================================================================
# FILE: timer.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import asyncio
from uuid import uuid4


class Timer(object):
    def __init__(self, loop):
        self._loop = loop
        self._handlers = {}

    def clear(self):
        """Removes all handlers in timer object."""
        ids = self._handlers.keys()
        for id in ids:
            self.remove_handler(id)

    def has_handler(self, id):
        """Checks whether or not the timer has a handler with the specified id.

        :returns: True if it has a handler, otherwise False
        """
        return id in self._handlers

    def add_handler(self, seconds, handler, *args, **kwargs):
        """Adds a new handler to be invoked no earlier than the specified
        number of seconds on an interval.

        :param seconds: The number of seconds to wait inbetween handler calls,
                        serving as a minimum (can take more time)
        :param handler: The handler to invoke
        :param args: The arguments to the handler
        :param kwargs: The keyword arguments to the handler
        :returns: The id of the newly-created handler
        """
        id = str(uuid4())
        self._handlers[id] = [seconds, handler, *args, *kwargs]
        self._add_handler(id, seconds, handler, *args, **kwargs)
        return id

    def _add_handler(self, id, seconds, handler, *args, **kwargs):
        """Adds a new handler to be invoked no earlier than the specified
        number of seconds on an interval.

        :param id: The id of the handler
        :param seconds: The number of seconds to wait inbetween handler calls,
                        serving as a minimum (can take more time)
        :param handler: The handler to invoke
        :param args: The arguments to the handler
        :param kwargs: The keyword arguments to the handler
        """
        @asyncio.coroutine
        def handler_wrapper():
            yield from asyncio.sleep(seconds)
            try:
                handler(*args, **kwargs)
            except Exception:
                self.remove_handler(id)
            self._add_handler(id, seconds, handler, *args, **kwargs)

        if (id in self._handlers):
            self._loop.create_task(handler_wrapper())

    def remove_handler(self, id):
        """Removes the handler with the specified id.

        :param id: The id of the handler
        :returns: True if the handler was removed, otherwise false if no
                  handler was found
        """
        return self._handlers.pop(id, None) is not None

    def get_handler_interval(self, id):
        """Returns the interval in seconds at which the handler is invoked.

        :param id: The id of the handler
        :returns: The number of seconds serving as the minimum time between
                  invocations of the handler, or None if handler is not found
        """
        return self._handlers[id][0] if (id in self._handlers) else None

    def get_handler_function(self, id):
        """Returns the function invoked by the handler.

        :param id: The id of the handler
        :returns: The function wrapped by the hander, or None if handler is
                  not found
        """
        return self._handlers[id][1] if (id in self._handlers) else None

    def get_handler_args(self, id):
        """Returns the args array provided to the handler.

        :param id: The id of the handler
        :returns: The array of arguments provided to the handler upon
                  invocation, or None if handler is not found
        """
        return self._handlers[id][2] if (id in self._handlers) else None

    def get_handler_kwargs(self, id):
        """Returns the keyword args dict provided to the handler.

        :param id: The id of the handler
        :returns: The dict of keyword arguments provided to the handler upon
                  invocation, or None if handler is not found
        """
        return self._handlers[id][3] if (id in self._handlers) else None
