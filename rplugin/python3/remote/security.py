# =============================================================================
# FILE: security.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================

from hmac import HMAC
from hashlib import sha256


def new_hmac_from_key(key, digestmod=sha256):
    """Creates a new hmac instance using the provided key.

    :param key: The key as a string
    :param digestmod: The hashlib function to use, defaulting to sha256
    :returns: The hmac instance
    """
    return HMAC(key.encode(), digestmod=digestmod)


def gen_signature(hmac, data):
    """Creates a signature from the provided hmac and given data.

    :param hmac: The hmac instance to use to create a digest
    :param data: Collection of data to use when producing the signature;
                 each element should be a collection of bytes
    :returns: A digest in the form of a string representing the signature
    """
    h = hmac.copy()
    for d in data:
        h.update(d)
    return h.digest()
