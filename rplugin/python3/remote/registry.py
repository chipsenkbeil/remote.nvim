# =============================================================================
# FILE: registry.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
from .messages.constants import (
    MESSAGE_SUBTYPE_REQUEST,
    MESSAGE_SUBTYPE_RESPONSE,
    MESSAGE_SUBTYPE_BROADCAST,
)


class MessageRegistry(object):
    def __init__(self):
        self._registry = {}

    def register(self, message_class):
        """Registers a message class by type and subtype.

        :param message_class: The class of the message to register
        """
        t = message_class._type

        # If no type found, exit
        if (t is None):
            return

        if (t not in self._registry):
            self._registry[t] = {}

        if (message_class.is_request()):
            self._registry[t][MESSAGE_SUBTYPE_REQUEST] = message_class
        if (message_class.is_response()):
            self._registry[t][MESSAGE_SUBTYPE_RESPONSE] = message_class
        if (message_class.is_broadcast()):
            self._registry[t][MESSAGE_SUBTYPE_BROADCAST] = message_class

    def lookup(self, msg_type, msg_subtype):
        """Looks up a message class by type and subtype.

        :param msg_type: The main type representing the class
        :param msg_subtype: The secondary type (request/response/broadcast)
                            representing the class
        :returns: A class object, or None if not found
        """
        d = self._registry
        if (msg_type in d and msg_subtype in d[msg_type]):
            return d[msg_type][msg_subtype]
        else:
            return None


class ActionRegistry(object):
    def __init__(self):
        self._registry = {}

    def register(self, message_class, action):
        """Registers an action to be performed when a message of the following
        class is received.

        :param message_class: The class of the message to be used as a lookup
        :param action: The function to invoke, taking the instance of the
                       message as an argument
        """
        self._registry[message_class.__name__] = action

    def lookup(self, message_instance):
        """Looks up an action by the name of the class of the message instance.

        :param message_instance: The instance of the message whose class name
                                 will be used to look up the associated action
        :returns: The action if found, otherwise None
        """
        key = message_instance.__class__.__name__
        return self._registry[key] if (key in self._registry) else None

    def process(self, message_instance):
        """Processes a message instance using the associated action.

        :param message_instance: The message to process using the associated
                                 action
        :returns: The result of the action, or None if no action found
        """
        action = self.lookup(message_instance)
        return action(message_instance) if (action is not None) else None
