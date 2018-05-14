# =============================================================================
# FILE: registry.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================


class ActionRegistry(object):
    def __init__(self):
        self._registry = {}

    def register(self, packet_type, action):
        """Registers an action to be performed when a packet of the following
        type is received.

        :param packet_type: The type of packet to be funneled to the specified
                            action
        :param action: The function to invoke, taking the instance of the
                       packet as an argument
        """
        self._registry[packet_type] = action

    def lookup(self, packet_type):
        """Looks up an action by the type of packet.

        :param packet_type: The type of packet to be whose associated action
                            to retrieve
        :returns: The action if found, otherwise None
        """
        key = packet_type
        return self._registry[key] if (key in self._registry) else None

    def process(self, packet):
        """Processes a packet instance using the associated action.

        :param packet: The packet to process
        :returns: The result of the action, or None if no action found
        """
        packet_type = packet.get_header().get_type()
        action = self.lookup(packet_type)
        return action(packet) if (action is not None) else None
