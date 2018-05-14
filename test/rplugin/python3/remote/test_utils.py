# =============================================================================
# FILE: test_utils.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
from remote.utils import (
    is_int,
    to_int,
)


def test_to_int_valid_string():
    expected = 999
    actual = to_int('  999  ')
    assert actual == expected


def test_to_int_invalid_string():
    expected = 'default'
    actual = to_int('abc', expected)
    assert actual == expected


def test_to_int_type_error():
    with pytest.raises(TypeError):
        to_int([])


def test_is_int_true():
    expected = True
    actual = is_int('999')
    assert actual == expected


def test_is_int_false():
    expected = False
    actual = is_int('abc')
    assert actual == expected
