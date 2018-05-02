import pytest
import msgpack
from remote.msg import *


class TestMetadata(object):
    def test_encode_passed_Metadata(self):
        m = Metadata().set_value('key', [1, 2, 3])
        o = Metadata.encode(m)
        assert o[Metadata.name()]
        assert o['_data'] == {'key': [1, 2, 3]}

    def test_encode_not_passed_Metadata(self):
        m = {'key': 'value'}
        o = Metadata.encode(m)
        assert o == m

    def test_set_value_already_set(self):
        m = Metadata()
        m.set_value('key', 0)
        m.set_value('key', 1)
        assert m.get_value('key') == 1

    def test_set_value_not_already_set(self):
        m = Metadata()
        m.set_value('key', 999)
        assert m.get_value('key') == 999

    def test_to_bytes_value_not_set(self):
        m = Metadata()
        b = m.to_bytes()

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = {}
        expected = msgpack.packb(expected, use_bin_type=True)

        assert b == expected

    def test_to_bytes_value_set(self):
        m = Metadata()
        m.set_value('key', 999)
        b = m.to_bytes()

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = m._data
        expected = msgpack.packb(expected, use_bin_type=True)

        assert b == expected

    def test_from_bytes_value_not_set(self):
        m = Metadata()

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = {}
        b = msgpack.packb(expected, use_bin_type=True)

        new_m = Metadata().from_bytes(b)

        assert m.to_dict() == new_m.to_dict()

    def test_from_bytes_value_set(self):
        m = Metadata()
        m.set_value('key', 999)

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = m._data
        b = msgpack.packb(expected, use_bin_type=True)

        new_m = Metadata().set_value('key', 0).from_bytes(b)

        assert m.to_dict() == new_m.to_dict()

    def test_to_dict(self):
        m = Metadata().set_value('key', 999)
        assert m.to_dict() == {'data': {'key': 999}}


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
