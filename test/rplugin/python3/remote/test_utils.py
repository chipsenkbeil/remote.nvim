# =============================================================================
# FILE: test_utils.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
from remote.utils import (
    find_subclasses,
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


def test_find_subclasses_not_a_class():
    with pytest.raises(AssertionError):
        find_subclasses(3)


def test_find_subclasses_no_subclasses():
    class A():
        pass

    assert len(find_subclasses(A)) == 0


def test_find_subclasses_top_level_subclasses_only():
    class A():
        pass

    class B(A):
        pass

    class C(B):
        pass

    subclasses = find_subclasses(A, include_indirect=False)
    assert len(subclasses) == 1
    assert B in subclasses
    assert C not in subclasses


def test_find_subclasses_multi_level_subclasses():
    class A():
        pass

    class B(A):
        pass

    class C(B):
        pass

    subclasses = find_subclasses(A, include_indirect=True)
    assert len(subclasses) == 2
    assert B in subclasses
    assert C in subclasses
