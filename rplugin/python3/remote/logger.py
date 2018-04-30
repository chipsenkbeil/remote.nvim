# ============================================================================
# FILE: logger.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# LICENSE: Apache 2.0 license
#
# ORIGINAL PROJECT: Remote <https://github.com/Shougo/deoplete.nvim>
# ORIGINAL AUTHOR: Tommy Allen <tommy at esdf.io>
# ORIGINAL LICENSE: MIT license
# ============================================================================
import sys
import logging
from functools import wraps

log_format = '%(asctime)s %(levelname)-8s [%(process)d] (%(name)s) %(message)s'
log_message_cooldown = 0.5

root = logging.getLogger('remote')
root.propagate = False
init = False


def getLogger(name):
    """Get a logger that is a child of the 'root' logger.
    """
    return root.getChild(name)


def setup(nvim, level, output_file=None):
    """Setup logging for Remote
    """
    global init
    if init:
        return
    init = True

    if output_file:
        formatter = logging.Formatter(log_format)
        handler = logging.FileHandler(filename=output_file)
        handler.setFormatter(formatter)
        root.addHandler(handler)

        level = str(level).upper()
        if level not in ('DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR',
                         'CRITICAL', 'FATAL'):
            level = 'DEBUG'
        root.setLevel(getattr(logging, level))

        try:
            import pkg_resources

            neovim_version = pkg_resources.get_distribution('neovim').version
        except ImportError:
            neovim_version = 'unknown'

        # TODO: Add remote#util#neovim_version
        log = getLogger('logging')
        log.info('--- Remote Log Start ---')
        log.info('%s, Python %s, neovim client %s',
                 # nvim.call('remote#util#neovim_version'),
                 '',
                 '.'.join(map(str, sys.version_info[:3])),
                 neovim_version)

        # TODO: Add remote#_logging_notified
        # TODO: Add remote#util#print_debug
        # if not nvim.vars.get('remote#_logging_notified'):
        #     nvim.vars['remote#_logging_notified'] = 1
        #     nvim.call('remote#util#print_debug', 'Logging to %s' % (
        #               output_file))


def logmethod(func):
    """Decorator for setting up the logger in LoggingMixin subclasses.

    This does not guarantee that log messages will be generated.  If
    `LoggingMixin.is_debug_enabled` is True, it will be propagated up to the
    root 'remote' logger.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not init or not self.is_debug_enabled:
            return
        if self._logger is None:
            name = getattr(self, 'name', 'unknown')

            # If no name specified, check if the default method is there
            if (name == 'unknown'):
                f_name = getattr(self, '_log_class_name', None)

                # If default name method available, use it as name
                if (callable(f_name)):
                    name = f_name()

            self._logger = getLogger(name)
        return func(self, *args, **kwargs)
    return wrapper


class LoggingMixin(object):
    """Class that adds logging functions to a subclass.
    """
    is_debug_enabled = False
    _logger = None  # type: logging.Logger

    def _log_class_name(self):
        """Represents the name of the class."""
        return self.__class__.__name__

    @logmethod
    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    @logmethod
    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    @logmethod
    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)
    warn = warning

    @logmethod
    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    @logmethod
    def exception(self, msg, *args, **kwargs):
        # This will not produce a log message if there is no exception to log.
        self._logger.exception(msg, *args, **kwargs)

    @logmethod
    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)
    fatal = critical
