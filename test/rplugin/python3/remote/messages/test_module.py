# =============================================================================
# FILE: test_module.py (for __init__.py)
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote import messages as msg
from remote.messages import packet_to_message
from remote.packet import (
    Content,
    Header,
    Metadata,
    Packet,
)


def test_init_registry():
    """It should set the registry and populate with all classes extending
    broadcast, request, or response.
    """
    from remote.messages import _init_registry
    _init_registry()

    from remote.messages import _registry
    assert _registry is not None

    from remote.messages.constants import (
        MESSAGE_TYPE_COMMAND,
        MESSAGE_TYPE_ERROR,
        MESSAGE_TYPE_FILE_LIST,
        MESSAGE_SUBTYPE_REQUEST,
        MESSAGE_SUBTYPE_RESPONSE,
        MESSAGE_SUBTYPE_BROADCAST,
    )

    # Verify a class from each category appears and that each subtype is also
    # accessible through the registry
    assert None is not (
        _registry.lookup(MESSAGE_TYPE_FILE_LIST, MESSAGE_SUBTYPE_REQUEST))
    assert None is not (
        _registry.lookup(MESSAGE_TYPE_COMMAND, MESSAGE_SUBTYPE_RESPONSE))
    assert None is not (
        _registry.lookup(MESSAGE_TYPE_ERROR, MESSAGE_SUBTYPE_BROADCAST))
