# =============================================================================
# FILE: test_error.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.msg import *
from remote.msgs import error
from remote.security import new_hmac_from_key


def test_new_sets_username():
    expected = 'senkwich'
    hmac = new_hmac_from_key('')
    m = error.new(
        hmac=hmac,
        username=expected,
        session='',
        exception=Exception(),
    )

    assert m.get_header().get_username() == expected


def test_new_sets_session():
    expected = 'mysession'
    hmac = new_hmac_from_key('')
    m = error.new(
        hmac=hmac,
        username='',
        session=expected,
        exception=Exception(),
    )

    assert m.get_header().get_session() == expected


def test_new_sets_exception_text():
    e = Exception('this is an exception')
    hmac = new_hmac_from_key('')
    m = error.new(
        hmac=hmac,
        username='',
        session='',
        exception=e,
    )

    expected = str(e)
    assert m.get_content().get_data() == expected


def test_new_sets_parent_header():
    expected = Header.empty()
    hmac = new_hmac_from_key('')
    m = error.new(
        hmac=hmac,
        username='',
        session='',
        exception=Exception(),
        parent_header=expected,
    )


def test_is_match_error():
    m = Message().set_header(Header().set_msg_type(error.MESSAGE_TYPE))
    assert error.is_match(m)


def test_is_match_not_error():
    m = Message().set_header(Header().set_msg_type('SOME_OTHER_TYPE'))
    assert not error.is_match(m)


def test_get_exception_text_for_value():
    expected = 'some exception turned into text'

    m = Message().set_content(Content().set_data(expected))
    actual = error.get_exception_text(m)

    assert actual == expected


def test_get_exception_text_for_nothing():
    expected = None

    m = Message().set_content(Content())
    actual = error.get_exception_text(m)

    assert actual == expected
