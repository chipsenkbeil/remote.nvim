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
