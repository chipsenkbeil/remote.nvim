# =============================================================================
# FILE: test_server.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import pytest
from remote.server import RemoteServer
from unittest.mock import patch

TEST_ADDR = ''
TEST_PORT = 0
TEST_KEY = 'key'


def test_server_init_hmac_from_key():
    s = RemoteServer(nvim=None, loop=None, addr=None, port=None, key='')
    assert s.hmac is not None


def test_server_init_nonempty_key():
    s = RemoteServer(nvim=None, loop=None, addr=None, port=None, key='')
    assert s.hmac is not None


def test_server_is_not_running():
    s = RemoteServer(nvim=None, loop=None, addr=None, port=None, key='')
    assert not s.is_running()


def test_server_is_running():
    s = RemoteServer(nvim=None, loop=None, addr=None, port=None, key='')
    assert s.hmac is not None
