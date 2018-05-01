import pytest
import msgpack
from remote.msg import *


class TestContent(object):
    def test_encode_passed_Content(self):
        c = Content().set_data([1, 2, 3])
        o = Content.encode(c)
        assert o[Content.name()]
        assert o['_data'] == c.get_data()

    def test_encode_not_passed_Content(self):
        c = {'key': 'value'}
        o = Content.encode(c)
        assert o == c

    def test_set_data_already_set(self):
        c = Content()
        c.set_data(0)
        with pytest.raises(AssertionError):
            c.set_data(1)

    def test_set_data_not_already_set(self):
        c = Content()
        c.set_data(999)
        assert c.get_data() == 999

    def test_to_bytes_data_not_set(self):
        c = Content()
        with pytest.raises(AssertionError):
            c.to_bytes()

    def test_to_bytes_data_set(self):
        c = Content()
        c.set_data(999)
        b = c.to_bytes()

        expected = {}
        expected[Content.name()] = True
        expected['_data'] = c.get_data()
        expected = msgpack.packb(expected, use_bin_type=True)

        assert b == expected

    def test_from_bytes_data_not_set(self):
        c = Content()
        c.set_data(999)

        expected = {}
        expected[Content.name()] = True
        expected['_data'] = c.get_data()
        b = msgpack.packb(expected, use_bin_type=True)

        new_c = Content().from_bytes(b)

        assert c.to_dict() == new_c.to_dict()

    def test_from_bytes_data_set(self):
        c = Content()
        c.set_data(999)

        expected = {}
        expected[Content.name()] = True
        expected['_data'] = c.get_data()
        b = msgpack.packb(expected, use_bin_type=True)

        with pytest.raises(AssertionError):
            Content().set_data(0).from_bytes(b)

    def test_to_dict(self):
        c = Content().set_data(999)
        assert c.to_dict() == {'data': 999}

