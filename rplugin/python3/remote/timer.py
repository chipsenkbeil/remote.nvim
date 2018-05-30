# =============================================================================
# FILE: timer.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import asyncio


class Timer(object):
    def __init__(self, loop, interval, stop_on_exception=False):
        """Creates a new timer instance.

        :param loop: The event loop to use when setting up the timer
        :param interval: The number of seconds to wait inbetween handler calls,
                         serving as a minimum (can take more time)
        """
        self._loop = loop
        self._running = False
        self._interval = interval
        self._exceptions = []
        self._stop_on_exception = stop_on_exception
        self._handler = None

    def set_handler(self, handler, *args, **kwargs):
        """Sets the handler to be invoked by the timer.

        :param handler: The handler to invoke
        :param args: The arguments to the handler
        :param kwargs: The keyword arguments to the handler
        :returns: The updated timer instance
        """
        assert self._handler is None, 'Handler has already been set!'

        async def handler_wrapper():
            while self._running:
                start_time = self._loop.time()
                try:
                    handler(*args, **kwargs)
                except Exception as ex:
                    if self._stop_on_exception:
                        self.stop()
                    else:
                        self._exceptions.append(ex)
                finally:
                    end_time = self._loop.time()
                    delay = max(0.0, self._interval - (end_time - start_time))
                    await asyncio.sleep(delay, loop=self._loop)

        self._handler = handler_wrapper
        return self

    def start(self):
        """Starts the timer.

        :returns: The updated timer instance
        """
        assert self._handler is not None, 'Handler has not been set!'
        self._running = True
        self._loop.create_task(self._handler())
        return self

    def stop(self):
        """Stops the timer.

        :returns: The updated timer instance
        """
        self._running = False
        return self

    def running(self):
        """Returns whether or not the timer is running.

        :returns: True if running, otherwise False
        """
        return self._running

    def interval(self):
        """Returns the interval in seconds at which the timer is invoked.

        :returns: The number of seconds serving as the minimum time between
                  invocations of the handler, or None if handler is not found
        """
        return self._interval

    def exceptions(self):
        """Returns the exceptions that have occurred as a list.

        :returns: A list of exceptions with the last being most recent
        """
        return self._exceptions

    def clear_exceptions(self):
        """Clears all exceptions stored by the timer.

        :returns: The updated timer
        """
        self._exceptions = []
        return self
