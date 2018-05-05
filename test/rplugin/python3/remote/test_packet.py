# =============================================================================
# FILE: test_packet.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================
import pytest
import msgpack
from datetime import datetime
from hmac import HMAC
from remote.packet import (
    Content,
    Header,
    Metadata,
    Packet,
)


@pytest.fixture()
def packet(header, parent_header, metadata, content):
    return (Packet()
            .set_header(header)
            .set_parent_header(parent_header)
            .set_metadata(metadata)
            .set_content(content))


@pytest.fixture()
def header():
    d = datetime.strptime('1990-04-27', '%Y-%m-%d')
    return (Header()
            .set_id('12345')
            .set_username('senkwich')
            .set_session('mysession')
            .set_date(d)
            .set_type('some_type')
            .set_version('1.0'))


@pytest.fixture()
def parent_header():
    d = datetime.strptime('1990-04-27', '%Y-%m-%d')
    return (Header()
            .set_id('12345')
            .set_username('senkwich')
            .set_session('mysession')
            .set_date(d)
            .set_type('some_type')
            .set_version('1.0'))


@pytest.fixture()
def metadata():
    return Metadata().set_value('key', 'value')


@pytest.fixture()
def content():
    return Content().set_data(999)


class TestPacket(object):
    def test_encode_passed_Packet(self, packet):
        o = Packet.encode(packet)
        assert o[Packet.name()]
        assert o['_signature'] == packet.get_signature()
        assert o['_header'] == packet.get_header()
        assert o['_parent_header'] == packet.get_parent_header()
        assert o['_metadata'] == packet.get_metadata()
        assert o['_content'] == packet.get_content()

    def test_encode_passed_Header(self, header):
        assert Packet.encode(header) == Header.encode(header)

    def test_encode_passed_Metadata(self, metadata):
        assert Packet.encode(metadata) == Metadata.encode(metadata)

    def test_encode_passed_Content(self, content):
        assert Packet.encode(content) == Content.encode(content)

    def test_encode_passed_normal_value(self):
        d = {'key': 'value'}
        o = Packet.encode(d)
        assert o == d

    def test_decode_passed_encoded_Packet(self, packet):
        e = Packet.encode(packet)
        o = Packet.decode(e)
        assert o.to_dict() == packet.to_dict()

    def test_decode_passed_encoded_Header(self, header):
        e = Packet.encode(header)
        o = Packet.decode(e)
        assert o.to_dict() == header.to_dict()

    def test_decode_passed_encoded_Metadata(self, metadata):
        e = Packet.encode(metadata)
        o = Packet.decode(e)
        assert o.to_dict() == metadata.to_dict()

    def test_decode_passed_encoded_Content(self, content):
        e = Packet.encode(content)
        o = Packet.decode(e)
        assert o.to_dict() == content.to_dict()

    def test_decode_passed_encoded_normal_value(self):
        d = {'key': 'value'}
        e = Packet.encode(d)
        o = Packet.decode(e)
        assert o == d

    def test_set_header_success(self, header):
        assert Packet().set_header(header).get_header() == header

    def test_set_parent_header_success(self, parent_header):
        expected = parent_header
        actual = Packet().set_parent_header(parent_header).get_parent_header()
        assert actual == expected

    def test_set_metadata_success(self, metadata):
        assert Packet().set_metadata(metadata).get_metadata() == metadata

    def test_set_content_success(self, content):
        assert Packet().set_content(content).get_content() == content

    def test_gen_signature_hmac_None(
        self,
        header,
        parent_header,
        metadata,
        content,
    ):
        p = (Packet()
             .set_header(header)
             .set_parent_header(parent_header)
             .set_metadata(metadata)
             .set_content(content))

        with pytest.raises(AssertionError):
            hmac = None
            p.gen_signature(hmac)

    def test_gen_signature_header_not_set(
        self,
        parent_header,
        metadata,
        content,
    ):
        p = (Packet()
             .set_parent_header(parent_header)
             .set_metadata(metadata)
             .set_content(content))

        with pytest.raises(AssertionError):
            hmac = HMAC(b'12345')
            p.gen_signature(hmac)

    def test_gen_signature_parent_header_not_set(
        self,
        header,
        metadata,
        content,
    ):
        p = (Packet()
             .set_header(header)
             .set_metadata(metadata)
             .set_content(content))

        with pytest.raises(AssertionError):
            hmac = HMAC(b'12345')
            p.gen_signature(hmac)

    def test_gen_signature_metadata_not_set(
        self,
        header,
        parent_header,
        content
    ):
        p = (Packet()
             .set_header(header)
             .set_parent_header(parent_header)
             .set_content(content))

        with pytest.raises(AssertionError):
            hmac = HMAC(b'12345')
            p.gen_signature(hmac)

    def test_gen_signature_content_not_set(
        self,
        header,
        parent_header,
        metadata
    ):
        p = (Packet()
             .set_header(header)
             .set_parent_header(parent_header)
             .set_metadata(metadata))

        with pytest.raises(AssertionError):
            hmac = HMAC(b'12345')
            p.gen_signature(hmac)

    def test_gen_signature_success(
        self,
        header,
        parent_header,
        metadata,
        content
    ):
        p = (Packet()
             .set_header(header)
             .set_parent_header(parent_header)
             .set_metadata(metadata)
             .set_content(content))

        hmac = HMAC(b'12345')
        p.gen_signature(hmac)

        assert p.get_signature() is not None

    def test_to_dict(self, header, parent_header, metadata, content):
        p = (Packet()
             .set_header(header)
             .set_parent_header(parent_header)
             .set_metadata(metadata)
             .set_content(content))
        p._signature = '12345'

        assert p.to_dict() == {
            'signature': '12345',
            'header': header,
            'parent_header': parent_header,
            'metadata': metadata,
            'content': content,
        }


class TestHeader(object):
    def test_encode_passed_Header(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_type('some_type')
             .set_version('1.0'))
        o = Header.encode(h)
        assert o[Header.name()]
        assert o['_id'] == h.get_id()
        assert o['_username'] == h.get_username()
        assert o['_session'] == h.get_session()
        assert o['_date'] == h.get_date()
        assert o['_type'] == h.get_type()
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
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_type('some_type')
             .set_version('1.0'))

        encoded = {}
        encoded[Header.name()] = True
        encoded['_id'] = h.get_id()
        encoded['_username'] = h.get_username()
        encoded['_session'] = h.get_session()
        encoded['_date'] = h.get_date()
        encoded['_type'] = h.get_type()
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

    def test_set_id_success(self):
        value = '12345'
        assert Header().set_id(value).get_id() == value

    def test_set_username_success(self):
        value = 'senkwich'
        assert Header().set_username(value).get_username() == value

    def test_set_session_success(self):
        value = 'mysession'
        assert Header().set_session(value).get_session() == value

    def test_set_date_success(self):
        value = datetime.strptime('1990-04-27', '%Y-%m-%d')
        assert Header().set_date(value).get_date() == value

    def test_set_type_success(self):
        value = 'some_type'
        assert Header().set_type(value).get_type() == value

    def test_set_version_success(self):
        value = '1.0'
        assert Header().set_version(value).get_version() == value

    def test_to_bytes_id_not_set_yet(self):
        h = (Header()
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_username_not_set_yet(self):
        h = (Header()
             .set_id('12345')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_session_not_set_yet(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_date_not_set_yet(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_type('some_type')
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_type_not_set_yet(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_version('1.0'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_version_not_set_yet(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type'))

        with pytest.raises(AssertionError):
            h.to_bytes()

    def test_to_bytes_everything_already_set(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_type('some_type')
             .set_version('1.0'))

        b = h.to_bytes()

        expected = {}
        expected[Header.name()] = True
        expected['_id'] = h.get_id()
        expected['_username'] = h.get_username()
        expected['_session'] = h.get_session()
        expected['_date'] = {
            '__datetime__': True,
            's': d.strftime('%Y%m%dT%H:%M:%S.%f'),
        }
        expected['_type'] = h.get_type()
        expected['_version'] = h.get_version()
        expected = msgpack.packb(expected, use_bin_type=True)

        assert b == expected

    def test_from_bytes_id_already_set(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_id('12345').from_bytes(b)

    def test_from_bytes_username_already_set(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_username('senkwich').from_bytes(b)

    def test_from_bytes_session_already_set(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_session('mysession').from_bytes(b)

    def test_from_bytes_date_already_set(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_date(d).from_bytes(b)

    def test_from_bytes_type_already_set(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_type('some_type').from_bytes(b)

    def test_from_bytes_version_already_set(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        with pytest.raises(AssertionError):
            Header().set_version('1.0').from_bytes(b)

    def test_from_bytes_nothing_set_yet(self):
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(datetime.strptime('1990-04-27', '%Y-%m-%d'))
             .set_type('some_type')
             .set_version('1.0'))
        b = h.to_bytes()

        # Load into a header with nothing yet set
        new_h = Header().from_bytes(b)

        assert h.to_dict() == new_h.to_dict()

    def test_to_dict(self):
        d = datetime.strptime('1990-04-27', '%Y-%m-%d')
        h = (Header()
             .set_id('12345')
             .set_username('senkwich')
             .set_session('mysession')
             .set_date(d)
             .set_type('some_type')
             .set_version('1.0'))
        assert h.to_dict() == {
            'id': '12345',
            'username': 'senkwich',
            'session': 'mysession',
            'date': d,
            'type': 'some_type',
            'version': '1.0',
        }


class TestMetadata(object):
    def test_encode_passed_Metadata(self):
        p = Metadata().set_value('key', [1, 2, 3])
        o = Metadata.encode(p)
        assert o[Metadata.name()]
        assert o['_data'] == {'key': [1, 2, 3]}

    def test_encode_not_passed_Metadata(self):
        p = {'key': 'value'}
        o = Metadata.encode(p)
        assert o == p

    def test_decode_passed_encoded_Metadata(self):
        d = {}
        d[Metadata.name()] = True
        d['_data'] = {'key': 'value'}

        p = Metadata.decode(d)
        assert p.get_value('key') == 'value'

    def test_decode_not_passed_encoded_Metadata(self):
        c = {'key': 'value'}
        o = Metadata.decode(c)
        assert o == c

    def test_set_value_already_set(self):
        p = Metadata()
        p.set_value('key', 0)
        p.set_value('key', 1)
        assert p.get_value('key') == 1

    def test_set_value_not_already_set(self):
        p = Metadata()
        p.set_value('key', 999)
        assert p.get_value('key') == 999

    def test_to_bytes_value_not_set(self):
        p = Metadata()
        b = p.to_bytes()

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = {}
        expected = msgpack.packb(expected, use_bin_type=True)

        assert b == expected

    def test_to_bytes_value_set(self):
        p = Metadata()
        p.set_value('key', 999)
        b = p.to_bytes()

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = p._data
        expected = msgpack.packb(expected, use_bin_type=True)

        assert b == expected

    def test_from_bytes_value_not_set(self):
        p = Metadata()

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = {}
        b = msgpack.packb(expected, use_bin_type=True)

        new_p = Metadata().from_bytes(b)

        assert p.to_dict() == new_p.to_dict()

    def test_from_bytes_value_set(self):
        p = Metadata()
        p.set_value('key', 999)

        expected = {}
        expected[Metadata.name()] = True
        expected['_data'] = p._data
        b = msgpack.packb(expected, use_bin_type=True)

        new_p = Metadata().set_value('key', 0).from_bytes(b)

        assert p.to_dict() == new_p.to_dict()

    def test_to_dict(self):
        p = Metadata().set_value('key', 999)
        assert p.to_dict() == {'data': {'key': 999}}


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
