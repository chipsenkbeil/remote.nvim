# =============================================================================
# FILE: __init__.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
from ..registry import MessageRegistry
from .base import BaseMessage

# A module-wide registry used to associate messages
# with related packets
registry = MessageRegistry()


def register(msg_class):
    """Registers a message class with the registry. Serves as a decorator.

    :param msg_class: The message class
    """
    assert issubclass(msg_class, BaseMessage), 'Class is not BaseMessage: %r' % msg_class
    registry.register(msg_class)
    return msg_class
