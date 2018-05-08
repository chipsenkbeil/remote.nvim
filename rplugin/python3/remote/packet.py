# =============================================================================
# FILE: packet.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import msgpack
from hmac import HMAC
from uuid import uuid4
from datetime import datetime
from . import security

# Maximum UDP datagram size for IPv4 is 65,507 bytes
MAX_PACKET_SIZE = 65507

# Below is 60 KiB bytes limit for content to ensure
# we have plenty of room for the header and metadata
MAX_CONTENT_SIZE = 61440  # 60 KiB (~3.97 KiB of bytes for header)

# Represents the version of packets supported
PACKET_VERSION = '0.1'


class Packet(object):
    _signature = None
    _header = None
    _parent_header = None
    _metadata = None
    _content = None

    @staticmethod
    def empty():
        return (Packet()
                .set_parent_header(Header.empty())
                .set_header(Header.empty())
                .set_metadata(Metadata.empty())
                .set_content(Content.empty()))

    @staticmethod
    def name():
        return '__packet__'

    @staticmethod
    def read(obj):
        """Reads the content into a new packet.

        :param obj: The content to read
        :returns: A new packet instance, or None if not valid type
        """
        m = None

        if (isinstance(obj, bytes)):
            m = Packet().from_bytes(obj)

        return m

    @staticmethod
    def encode(obj):
        if (isinstance(obj, Packet)):
            d = {}
            d[Packet.name()] = True
            d['_signature'] = obj._signature
            d['_header'] = obj._header
            d['_parent_header'] = obj._parent_header
            d['_metadata'] = obj._metadata
            d['_content'] = obj._content
            return d
        obj = Header.encode(obj)
        obj = Metadata.encode(obj)
        obj = Content.encode(obj)
        return obj

    @staticmethod
    def decode(obj):
        if (Packet.name() in obj):
            m = Packet()
            m._signature = obj['_signature']
            m._header = obj['_header']
            m._parent_header = obj['_parent_header']
            m._metadata = obj['_metadata']
            m._content = obj['_content']
            return m

        if (isinstance(obj, dict)):
            obj = Header.decode(obj)
        if (isinstance(obj, dict)):
            obj = Metadata.decode(obj)
        if (isinstance(obj, dict)):
            obj = Content.decode(obj)
        return obj

    def set_header(self, header):
        self._header = header
        return self

    def get_header(self):
        return self._header

    def set_parent_header(self, parent_header):
        self._parent_header = parent_header
        return self

    def get_parent_header(self):
        return self._parent_header

    def set_metadata(self, metadata):
        self._metadata = metadata
        return self

    def get_metadata(self):
        return self._metadata

    def set_content(self, content):
        self._content = content
        return self

    def get_content(self):
        return self._content

    def gen_signature(self, hmac):
        """Generates a signature for the packet based on its properties."""
        self._signature = self._gen_signature(hmac)
        return self

    def _gen_signature(self, hmac):
        assert isinstance(hmac, HMAC)
        assert self._header is not None
        assert self._parent_header is not None
        assert self._metadata is not None
        assert self._content is not None

        return security.gen_signature(hmac, [
            self._header.to_bytes(),
            self._parent_header.to_bytes(),
            self._metadata.to_bytes(),
            self._content.to_bytes(),
        ])

    def get_signature(self):
        return self._signature

    def is_signature_valid(self, hmac):
        """Indicates whether the signature of the packet is valid."""
        sig = self._gen_signature(hmac)
        return self._signature == sig

    def to_bytes(self):
        """Converts packet into bytes."""
        assert self._signature is not None
        assert self._header is not None
        assert self._parent_header is not None
        assert self._metadata is not None
        assert self._content is not None
        return msgpack.packb(self, default=Packet.encode, use_bin_type=True)

    def from_bytes(self, b):
        """Fills in packet using bytes."""
        assert self._signature is None
        assert self._header is None
        assert self._parent_header is None
        assert self._metadata is None
        assert self._content is None

        packet = msgpack.unpackb(b, object_hook=Packet.decode, raw=False)
        self._signature = packet._signature
        self._header = packet._header
        self._parent_header = packet._parent_header
        self._metadata = packet._metadata
        self._content = packet._content
        return self

    def to_dict(self):
        """Converts packet into dictionary."""
        return {
            'signature': self._signature,
            'header': self._header,
            'parent_header': self._parent_header,
            'metadata': self._metadata,
            'content': self._content,
        }

    def __str__(self):
        return self.name() + ': ' + str(self.to_dict())


class Header(object):
    _id = None
    _username = None
    _session = None
    _date = None
    _type = None
    _version = None

    @staticmethod
    def empty():
        return (Header()
                .set_id('')
                .set_username('')
                .set_session('')
                .set_date_now()
                .set_type('')
                .set_version(''))

    @staticmethod
    def name():
        return '__header__'

    @staticmethod
    def encode(obj):
        if (isinstance(obj, Header)):
            d = {}
            d[Header.name()] = True
            d['_id'] = obj._id
            d['_username'] = obj._username
            d['_session'] = obj._session
            d['_date'] = obj._date
            d['_type'] = obj._type
            d['_version'] = obj._version
            return d
        elif (isinstance(obj, datetime)):
            return {
                '__datetime__': True,
                's': obj.strftime('%Y%m%dT%H:%M:%S.%f'),
            }
        return obj

    @staticmethod
    def decode(obj):
        if (Header.name() in obj):
            m = Header()
            m._id = obj['_id']
            m._username = obj['_username']
            m._session = obj['_session']
            m._date = obj['_date']
            m._type = obj['_type']
            m._version = obj['_version']
            return m
        elif ('__datetime__' in obj):
            return datetime.strptime(
                obj['s'],
                '%Y%m%dT%H:%M:%S.%f'
            )
        return obj

    def set_random_id(self):
        self.set_id(str(uuid4()))
        return self

    def set_id(self, id):
        self._id = id
        return self

    def get_id(self):
        return self._id

    def set_username(self, username):
        self._username = username
        return self

    def get_username(self):
        return self._username

    def set_session(self, session):
        self._session = session
        return self

    def get_session(self):
        return self._session

    def set_date_now(self):
        self.set_date(datetime.now())
        return self

    def set_date(self, date):
        self._date = date
        return self

    def get_date(self):
        return self._date

    def set_type(self, type):
        self._type = type
        return self

    def get_type(self):
        return self._type

    def set_version(self, version):
        self._version = version
        return self

    def get_version(self):
        return self._version

    def to_bytes(self):
        """Converts header into bytes."""
        assert self._id is not None
        assert self._username is not None
        assert self._session is not None
        assert self._date is not None
        assert self._type is not None
        assert self._version is not None
        return msgpack.packb(self, default=Header.encode, use_bin_type=True)

    def from_bytes(self, b):
        """Fills in header using bytes."""
        assert self._id is None
        assert self._username is None
        assert self._session is None
        assert self._date is None
        assert self._type is None
        assert self._version is None

        header = msgpack.unpackb(b, object_hook=Header.decode, raw=False)
        self._id = header._id
        self._username = header._username
        self._session = header._session
        self._date = header._date
        self._type = header._type
        self._version = header._version
        return self

    def to_dict(self):
        """Converts header into dictionary."""
        return {
            'id': self._id,
            'username': self._username,
            'session': self._session,
            'date': self._date,
            'type': self._type,
            'version': self._version,
        }

    def __str__(self):
        return self.name() + ': ' + str(self.to_dict())


class Metadata(object):
    _data = None

    @staticmethod
    def empty():
        return Metadata()

    @staticmethod
    def name():
        return '__metadata__'

    @staticmethod
    def encode(obj):
        if (isinstance(obj, Metadata)):
            d = {}
            d[Metadata.name()] = True
            d['_data'] = obj._data
            return d
        return obj

    @staticmethod
    def decode(obj):
        if (Metadata.name() in obj):
            m = Metadata()
            m._data = obj['_data']
            return m
        return obj

    def __init__(self):
        self._data = {}

    def set_value(self, key, value):
        self._data[key] = value
        return self

    def get_value(self, key):
        return self._data[key] if (key in self._data) else None

    def to_bytes(self):
        return msgpack.packb(self, default=Metadata.encode, use_bin_type=True)

    def from_bytes(self, b):
        metadata = msgpack.unpackb(b, object_hook=Metadata.decode, raw=False)
        self._data = metadata._data
        return self

    def to_dict(self):
        """Converts metadata into dictionary."""
        return {
            'data': self._data,
        }

    def __str__(self):
        return self.name() + ': ' + str(self.to_dict())


class Content(object):
    _data = None

    @staticmethod
    def empty():
        return Content().set_data(0)

    @staticmethod
    def name():
        return '__content__'

    @staticmethod
    def encode(obj):
        if (isinstance(obj, Content)):
            d = {}
            d[Content.name()] = True
            d['_data'] = obj._data
            return d
        return obj

    @staticmethod
    def decode(obj):
        if (Content.name() in obj):
            return Content().set_data(obj['_data'])
        return obj

    def set_data(self, data):
        self._data = data
        return self

    def get_data(self):
        return self._data

    def to_bytes(self):
        assert self._data is not None
        return msgpack.packb(self, default=Content.encode, use_bin_type=True)

    def from_bytes(self, b):
        assert self._data is None
        content = msgpack.unpackb(b, object_hook=Content.decode, raw=False)
        self._data = content._data
        return self

    def to_dict(self):
        """Converts content into dictionary."""
        return {
            'data': self._data,
        }

    def __str__(self):
        return self.name() + ': ' + str(self.to_dict())
