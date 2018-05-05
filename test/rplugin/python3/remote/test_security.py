# =============================================================================
# FILE: test_security.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
from remote.security import (
    gen_signature,
    new_hmac_from_key,
)


def test_new_hmac_from_key_where_key_not_string():
    with pytest.raises(AssertionError):
        new_hmac_from_key(12345)


def test_gen_signature():
    expected = b'#\xb0C\x1c\xd45D\xfc\x9e\xd7\xe6\x86\x01\x1d~\xa2\xd8\x0c\xbd\x17\xafC\xdf\x97\x0b\xd3\x89\xe3\x85\xfe\xfb\xc0'
    hmac = new_hmac_from_key('12345')
    actual = gen_signature(hmac, [b'a', b'b', b'c'])

    assert actual == expected
