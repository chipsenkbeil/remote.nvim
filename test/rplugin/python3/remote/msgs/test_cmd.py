# =============================================================================
# FILE: test_cmd.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.msg import *
from remote.msgs import cmd
from remote.security import new_hmac_from_key


def test_new_sets_username():
    expected = 'senkwich'
    hmac = new_hmac_from_key('')
    m = cmd.new(
        hmac=hmac,
        username=expected,
        session='',
        name='',
        args='',
    )

    assert m.get_header().get_username() == expected


def test_new_sets_session():
    expected = 'mysession'
    hmac = new_hmac_from_key('')
    m = cmd.new(
        hmac=hmac,
        username='',
        session=expected,
        name='',
        args='',
    )

    assert m.get_header().get_session() == expected


def test_new_sets_name():
    expected = 'CmdName'
    hmac = new_hmac_from_key('')
    m = cmd.new(
        hmac=hmac,
        username='',
        session='',
        name=expected,
        args='',
    )

    assert m.get_metadata().get_value(cmd.CMD_METADATA_NAME) == expected


def test_new_sets_args():
    expected = 'arg1 arg2 3 4 ;;1aksdfk43 q34 \' \' asdlfkj2'
    hmac = new_hmac_from_key('')
    m = cmd.new(
        hmac=hmac,
        username='',
        session='',
        name='',
        args=expected,
    )

    assert m.get_metadata().get_value(cmd.CMD_METADATA_ARGS) == expected


def test_new_sets_parent_header():
    expected = Header.empty()
    hmac = new_hmac_from_key('')
    m = cmd.new(
        hmac=hmac,
        username='',
        session='',
        name='',
        args='',
        parent_header=expected,
    )


def test_is_match_cmd():
    m = Message().set_header(Header().set_msg_type(cmd.MESSAGE_TYPE))
    assert cmd.is_match(m)


def test_is_match_not_cmd():
    m = Message().set_header(Header().set_msg_type('SOME_OTHER_TYPE'))
    assert not cmd.is_match(m)


def test_get_name_for_value():
    expected = 'CmdName'

    m = Message().set_metadata(Metadata().set_value(
        cmd.CMD_METADATA_NAME, expected))
    actual = cmd.get_name(m)

    assert actual == expected


def test_get_name_for_nothing():
    expected = None

    m = Message().set_metadata(Metadata())
    actual = cmd.get_name(m)

    assert actual == expected


def test_get_args_for_value():
    expected = 'arg1 arg2 arg3'

    m = Message().set_metadata(Metadata().set_value(
        cmd.CMD_METADATA_ARGS, expected))
    actual = cmd.get_args(m)

    assert actual == expected


def test_get_args_for_nothing():
    expected = None

    m = Message().set_metadata(Metadata())
    actual = cmd.get_args(m)

    assert actual == expected
