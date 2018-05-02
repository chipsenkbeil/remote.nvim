import pytest
import msgpack
import datetime
from remote.msg import *

class TestHeader(object):

    def test_encode_passed_Header(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_msg_type('some_type')
             .set_version('1.0'))
        o = Header.encode(h)
        assert o[Header.name()]
        assert o['_msg_id'] == h.get_msg_id()
        assert o['_username'] == h.get_username()
        assert o['_session'] == h.get_session()
        assert o['_date'] == h.get_date()
        assert o['_msg_type'] == h.get_msg_type()
        assert o['_version'] == h.get_version()

    def test_encode_passed_datetime(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        o = Header.encode(d)
        assert o['__datetime__']
        assert o['s'] == d.strftime('%Y%m%dT%H:%M:%S.%f')

    def test_encode_not_passed_Header_or_datetime(self):
        d = {'key': 'value'}
        o = Header.encode(d)
        assert o == d

    def test_decode_passed_encoded_Header(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_msg_type('some_type')
             .set_version('1.0'))

        encoded = {}
        encoded[Header.name()] = True
        encoded['_msg_id'] = h.get_msg_id()
        encoded['_username'] = h.get_username()
        encoded['_session'] = h.get_session()
        encoded['_date'] = h.get_date()
        encoded['_msg_type'] = h.get_msg_type()
        encoded['_version'] = h.get_version()

        new_h = Header.decode(encoded)
        assert new_h.to_dict() == h.to_dict()

    def test_decode_passed_encoded_datetime(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        encoded = {
            '__datetime__': True,
            's': d.strftime('%Y%m%dT%H:%M:%S.%f'),
        }
        new_d = Header.decode(encoded)
        assert new_d == d

    def test_decode_not_passed_encoded_Header_or_datetime(self):
        d = {'key': 'value'}
        o = Header.decode(d)
        assert o == d

    def test_set_msg_id_not_string(self):
        with pytest.raises(AssertionError):
            Header().set_msg_id(12345)

    def test_set_msg_id_already_set(self):
        with pytest.raises(AssertionError):
            Header().set_msg_id('12345').set_msg_id('12345')

    def test_set_msg_id_success(self):
        value = '12345'
        assert Header().set_msg_id(value).get_msg_id() == value

    def test_set_username_not_string(self):
        with pytest.raises(AssertionError):
            Header().set_username(12345)

    def test_set_username_already_set(self):
        with pytest.raises(AssertionError):
            Header().set_username('senkwich').set_username('senkwich')

    def test_set_username_success(self):
        value = 'senkwich'
        assert Header().set_username(value).get_username() == value

    def test_set_session_not_string(self):
        with pytest.raises(AssertionError):
            Header().set_session(12345)

    def test_set_session_already_set(self):
        with pytest.raises(AssertionError):
            Header().set_session('mysession').set_session('mysession')

    def test_set_session_success(self):
        value = 'mysession'
        assert Header().set_session(value).get_session() == value

    def test_set_date_not_datetime(self):
        with pytest.raises(AssertionError):
            Header().set_date('1990/04/27')

    def test_set_date_already_set(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        with pytest.raises(AssertionError):
            Header().set_date(d).set_date(d)

    def test_set_date_success(self):
        value = datetime.strptime('1990-04-27', '%Y-%m-%d')
        assert Header().set_date(value).get_date() == value

    def test_set_msg_type_not_string(self):
        with pytest.raises(AssertionError):
            Header().set_msg_type(12345)

    def test_set_msg_type_already_set(self):
        with pytest.raises(AssertionError):
            Header().set_msg_type('some_type').set_msg_type('some_type')

    def test_set_msg_type_success(self):
        value = 'some_type'
        assert Header().set_msg_type(value).get_msg_type() == value

    def test_set_version_not_string(self):
        with pytest.raises(AssertionError):
            Header().set_version(12345)

    def test_set_version_already_set(self):
        with pytest.raises(AssertionError):
            Header().set_version('1.0').set_version('1.0')

    def test_set_version_success(self):
        value = '1.0'
        assert Header().set_version(value).get_version() == value

    def test_to_bytes_msg_id_not_set_yet(self):
        h = (Header()
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_username_not_set_yet(self):
        h = (Header()
             .set_msg_id('12345')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_session_not_set_yet(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_date_not_set_yet(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_msg_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_msg_type_not_set_yet(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_version_not_set_yet(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_everything_already_set(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_msg_type('some_type')
             .set_version('1.0'))

        b = h.to_bytes()

        expected = {}
        expected[Header.name()] = True
        expected['_msg_id'] = h.get_msg_id()
        expected['_username'] = h.get_username()
        expected['_session'] = h.get_session()
        expected['_date'] = {
            '__datetime__': True,
            's': d.strftime('%Y%m%dT%H:%M:%S.%f'),
        }
        expected['_msg_type'] = h.get_msg_type()
        expected['_version'] = h.get_version()
        expected = msgpack.packb(expected, use_bin_type=True)

        assert b == expected

    def test_from_bytes_msg_id_already_set(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_msg_id('12345').from_bytes(b)

    def test_from_bytes_username_already_set(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_username('senkwich').from_bytes(b)

    def test_from_bytes_session_already_set(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_session('mysession').from_bytes(b)

    def test_from_bytes_date_already_set(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_msg_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_date(d).from_bytes(b)

    def test_from_bytes_msg_type_already_set(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_msg_type('some_type').from_bytes(b)

    def test_from_bytes_version_already_set(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_version('1.0').from_bytes(b)

    def test_from_bytes_nothing_set_yet(self):
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_msg_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        # Load into a header with nothing yet set
        new_h = Header().from_bytes(b)

        assert h.to_dict() == new_h.to_dict()

    def test_to_dict(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_msg_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_msg_type('some_type')
             .set_version('1.0'))
        assert h.to_dict() == {
            'msg_id': '12345',
            'username': 'senkwich',
            'session': 'mysession',
            'date': d,
            'msg_type': 'some_type',
            'version': '1.0',
        }


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

    def test_decode_passed_encoded_Metadata(self):
        d = {}
        d[Metadata.name()] = True
        d['_data'] = {'key': 'value'}

        m = Metadata.decode(d)
        assert m.get_value('key') == 'value'

    def test_decode_not_passed_encoded_Metadata(self):
        c = {'key': 'value'}
        o = Metadata.decode(c)
        assert o == c

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

    def test_decode_passed_encoded_Content(self):
        d = {}
        d[Content.name()] = True
        d['_data'] = 999

        c = Content.decode(d)
        assert c.get_data() == 999

    def test_decode_not_passed_encoded_Content(self):
        c = {'key': 'value'}
        o = Content.decode(c)
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

    def test_from_bytes_nothing_set_yet(self):
        c = Content()
        c.set_data(999)

        b = c.to_bytes()

        new_c = Content().from_bytes(b)

        assert c.to_dict() == new_c.to_dict()

    def test_from_bytes_data_already_set(self):
        c = Content()
        c.set_data(999)

        b = c.to_bytes()

        with pytest.raises(AssertionError):
            Content().set_data(0).from_bytes(b)

    def test_to_dict(self):
        c = Content().set_data(999)
        assert c.to_dict() == {'data': 999}
