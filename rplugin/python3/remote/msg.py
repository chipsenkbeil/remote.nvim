# =============================================================================
# FILE: msg.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import msgpack
from uuid import uuid4
from datetime import datetime
from remote import security

# Maximum UDP datagram size is 65,507
MAX_CONTENT_SIZE = 40000


class Message(object):
    _signature = None
    _header = None
    _parent_header = None
    _metadata = None
    _content = None

    @staticmethod
    def encode(obj):
        return obj

    @staticmethod
    def decode(obj):
        return obj

    def set_header(self, header):
        assert isinstance(header, Header)
        assert self._header is None
        self._header = header
        return self

    def get_header(self):
        return self._header

    def set_parent_header(self, parent_header):
        assert isinstance(parent_header, Header)
        assert self._parent_header is None
        self._parent_header = parent_header
        return self

    def get_parent_header(self):
        return self._parent_header

    def set_metadata(self, metadata):
        assert isinstance(metadata, Metadata)
        assert self._metadata is None
        self._metadata = metadata
        return self

    def get_metadata(self):
        return self._metadata

    def set_content(self, content):
        assert self._content is None
        self._content = content
        return self

    def get_content(self):
        return self._content

    def gen_signature(self, hmac):
        """Generates a signature for the message based on its properties."""
        assert self._signature is None
        self._signature = self._gen_signature(hmac)

    def _gen_signature(self, hmac):
        assert self._header is not None
        assert self._parent_header is not None
        assert self._metadata is not None
        assert self._content is not None

        return security.gen_signature(hmac, [
            self._header.toBytes(),
            self._parent_header.toBytes(),
            self._metadata.toBytes(),
            self._content.toBytes(),
        ])

    def get_signature(self):
        return self._signature

    def is_signature_valid(self, hmac):
        """Indicates whether the signature of the message is valid."""
        sig = self._genSignature(hmac)
        return self._signature == sig

    def to_bytes(self):
        """Converts message into bytes."""
        assert self._signature is not None
        assert self._header is not None
        assert self._parent_header is not None
        assert self._metadata is not None
        assert self._content is not None
        return msgpack.packb(self, default=Message.encode, use_bin_type=True)

    def from_bytes(self, b):
        """Fills in message using bytes."""
        assert self._signature is None
        assert self._header is None
        assert self._parent_header is None
        assert self._metadata is None
        assert self._content is None

        msg = msgpack.unpackb(b, object_hook=Message.decode, raw=False)
        self._signature = msg._signature
        self._header = msg._header
        self._parent_header = msg._parent_header
        self._metadata = msg._metadata
        self._content = msg._content
        return self

    def to_dict(self):
        """Converts message into dictionary."""
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
    _msg_id = None
    _username = None
    _session = None
    _date = None
    _msg_type = None
    _version = None

    @staticmethod
    def name():
        return '__header__'

    @staticmethod
    def encode(obj):
        if (isinstance(obj, Header)):
            d = {}
            d[Header.name()] = True
            d['_msg_id'] = obj._msg_id
            d['_username'] = obj._username
            d['_session'] = obj._session
            d['_date'] = obj._date
            d['_msg_type'] = obj._msg_type
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
            m._msg_id = obj['_msg_id']
            m._username = obj['_username']
            m._session = obj['_session']
            m._date = obj['_date']
            m._msg_type = obj['_msg_type']
            m._version = obj['_version']
            return m
        elif ('__datetime__' in obj):
            return datetime.strptime(
                obj['s'],
                '%Y%m%dT%H:%M:%S.%f'
            )
        return obj

    def set_random_msg_id(self):
        self.set_msg_id(uuid4())
        return self

    def set_msg_id(self, msg_id):
        assert isinstance(msg_id, str)
        assert self._msg_id is None
        self._msg_id = msg_id
        return self

    def get_msg_id(self):
        return self._msg_id

    def set_username(self, username):
        assert isinstance(username, str)
        assert self._username is None
        self._username = username
        return self

    def get_username(self):
        return self._username

    def set_session(self, session):
        assert isinstance(session, str)
        assert self._session is None
        self._session = session
        return self

    def get_session(self):
        return self._session

    def set_date(self, date):
        assert isinstance(date, datetime)
        assert self._date is None
        self._date = date
        return self

    def get_date(self):
        return self._date

    def set_msg_type(self, msg_type):
        assert isinstance(msg_type, str)
        assert self._msg_type is None
        self._msg_type = msg_type
        return self

    def get_msg_type(self):
        return self._msg_type

    def set_version(self, version):
        assert isinstance(version, str)
        assert self._version is None
        self._version = version
        return self

    def get_version(self):
        return self._version

    def to_bytes(self):
        """Converts header into bytes."""
        assert self._msg_id is not None
        assert self._username is not None
        assert self._session is not None
        assert self._date is not None
        assert self._msg_type is not None
        assert self._version is not None
        return msgpack.packb(self, default=Header.encode, use_bin_type=True)

    def from_bytes(self, b):
        """Fills in header using bytes."""
        assert self._msg_id is None
        assert self._username is None
        assert self._session is None
        assert self._date is None
        assert self._msg_type is None
        assert self._version is None

        header = msgpack.unpackb(b, object_hook=Header.decode, raw=False)
        self._msg_id = header._msg_id
        self._username = header._username
        self._session = header._session
        self._date = header._date
        self._msg_type = header._msg_type
        self._version = header._version
        return self

    def to_dict(self):
        """Converts header into dictionary."""
        return {
            'msg_id': self._msg_id,
            'username': self._username,
            'session': self._session,
            'date': self._date,
            'msg_type': self._msg_type,
            'version': self._version,
        }

    def __str__(self):
        return self.name() + ': ' + str(self.to_dict())


class Metadata(object):
    _data = None

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
        assert self._data is None
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
