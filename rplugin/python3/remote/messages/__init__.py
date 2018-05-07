# =============================================================================
# FILE: __init__.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import os
from ..utils import find_subclasses, load_all_modules

# Contains a registry that will be loaded upon first
# trying to convert a packet to a message
global _registry
_registry = None


def _init_registry():
    """Initializes the registry of messages."""
    global _registry

    BASE_DIR = os.path.dirname(__file__)
    PACKAGE = __package__

    # Skip if trying to reload this module
    EXCLUSIONS = [PACKAGE + '.__init__']

    from ..registry import MessageRegistry
    _registry = MessageRegistry()

    for mod in load_all_modules(BASE_DIR, PACKAGE, EXCLUSIONS):
        print('Loaded {}'.format(mod))

    from .base import (
        BaseBroadcastMessage,
        BaseRequestMessage,
        BaseResponseMessage,
    )
    classes_to_register = []
    classes_to_register.extend(find_subclasses(BaseBroadcastMessage))
    classes_to_register.extend(find_subclasses(BaseRequestMessage))
    classes_to_register.extend(find_subclasses(BaseResponseMessage))
    for cl in classes_to_register:
        _registry.register(cl)


def packet_to_message(packet):
    """Converts a packet to its corresponding message.

    :param packet: The packet to convert
    :returns: The message instance, or None if no matching message found
    """
    global _registry

    if _registry is None:
        _init_registry()

    from .constants import MESSAGE_SUBTYPE

    msg_class = _registry.lookup(
        packet.get_header().get_type(),
        packet.get_metadata().get_value(MESSAGE_SUBTYPE),
    )

    msg = msg_class.from_packet(packet) if (msg_class is not None) else None
    if (msg is not None and packet.get_parent_header() is not None):
        from .base import BaseMessage
        # NOTE: Cannot create more specific message as subtype is in metadata
        #       and lost when submitted in packet; look into converting this
        #       structure into not using a parent message
        msg._parent = BaseMessage(
            id=packet.get_parent_header().get_id(),
            username=packet.get_parent_header().get_username(),
            session=packet.get_parent_header().get_session(),
        )
        msg._parent._type = packet.get_parent_header().get_type()

    return msg
