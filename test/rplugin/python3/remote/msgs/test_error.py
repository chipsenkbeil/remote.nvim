# =============================================================================
# FILE: test_error.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.packet import *
from remote.msgs import error


def test_new_sets_username():
    expected = 'senkwich'
    m = error.new(
        username=expected,
        session='',
        exception=Exception(),
    )

    assert m.get_header().get_username() == expected


def test_new_sets_session():
    expected = 'mysession'
    m = error.new(
        username='',
        session=expected,
        exception=Exception(),
    )

    assert m.get_header().get_session() == expected


def test_new_sets_exception_text():
    e = Exception('this is an exception')
    m = error.new(
        username='',
        session='',
        exception=e,
    )

    expected = str(e)
    assert m.get_content().get_data() == expected


def test_new_sets_parent_header():
    expected = Header.empty()
    m = error.new(
        username='',
        session='',
        exception=Exception(),
        parent_header=expected,
    )

    assert m.get_parent_header() == expected


def test_is_match_error():
    m = Packet().set_header(Header().set_type(error.MESSAGE_TYPE))
    assert error.is_match(m)


def test_is_match_not_error():
    m = Packet().set_header(Header().set_type('SOME_OTHER_TYPE'))
    assert not error.is_match(m)


def test_get_exception_text_for_value():
    expected = 'some exception turned into text'

    m = Packet().set_content(Content().set_data(expected))
    actual = error.get_exception_text(m)

    assert actual == expected


def test_get_exception_text_for_nothing():
    expected = None

    m = Packet().set_content(Content())
    actual = error.get_exception_text(m)

    assert actual == expected
