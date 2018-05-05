# =============================================================================
# FILE: utils.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================


def to_int(s, default=None):
    """Attempts to convert the provided string to an integer.

    :param s: The text to convert
    :param default: Default value to return if cannot be converted
    :returns: The integer if converted, otherwise the default value
    """
    try:
        return int(s)
    except ValueError:
        pass

    return default


def is_int(s):
    """Checks if the provided string is an integer.

    :param s: The text to check
    :returns: True if an integer, otherwise False
    """
    return to_int(s) is not None


def find_subclasses(cl):
    """Finds all classes that subclass the provided class, even indirectly.

    :param cl: The class whose subclasses to find
    :returns: A list of class objects representing the subclasses
    """
    assert isinstance(cl, type)

    class_list = []
    queue = []

    # Enqueue top-level class
    queue.append(cl)

    while (len(queue) > 0):
        next_class = queue.pop(0)  # Dequeue next class to search
        class_list.append(next_class)
        queue.extend(next_class.__subclasses__())

    # Return all classes but the first since that is the class we started with
    return class_list[1:]
