# =============================================================================
# FILE: test_sync.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
from remote.packet import *
from remote.msgs import sync


def test_new_send_sets_username():
    expected = 'senkwich'
    m = sync.new_send(
        username=expected,
        session='',
        filename='',
        count=1,
        index=0,
        data=b'',
        length=1,
    )

    assert m.get_header().get_username() == expected


def test_new_send_sets_session():
    expected = 'mysession'
    m = sync.new_send(
        username='',
        session=expected,
        filename='',
        count=1,
        index=0,
        data=b'',
        length=1,
    )

    assert m.get_header().get_session() == expected


def test_new_send_sets_filename():
    expected = 'my file'
    m = sync.new_send(
        username='',
        session='',
        filename=expected,
        count=1,
        index=0,
        data=b'',
        length=1,
    )

    assert m.get_metadata().get_value(sync.SYNC_METADATA_FILENAME) == expected


def test_new_send_sets_chunk_count():
    expected = 999
    m = sync.new_send(
        username='',
        session='',
        filename='',
        count=expected,
        index=0,
        data=b'',
        length=1,
    )

    assert m.get_metadata().get_value(sync.SYNC_METADATA_CHUNK_COUNT) == expected


def test_new_send_sets_chunk_index():
    expected = 999
    m = sync.new_send(
        username='',
        session='',
        filename='',
        count=1,
        index=expected,
        data=b'',
        length=1,
    )

    assert m.get_metadata().get_value(sync.SYNC_METADATA_CHUNK_INDEX) == expected


def test_new_send_sets_data():
    expected = b'some data bytes'
    m = sync.new_send(
        username='',
        session='',
        filename='',
        count=1,
        index=0,
        data=expected,
        length=len(expected),
    )

    assert m.get_content().get_data() == expected


def test_new_send_sets_data_using_length():
    data = b'some data bytes'
    length = int(len(data) / 2)
    m = sync.new_send(
        username='',
        session='',
        filename='',
        count=1,
        index=0,
        data=data,
        length=length,
    )

    expected = data[0:length]
    assert m.get_content().get_data() == expected


def test_new_send_sets_parent_header():
    expected = Header.empty()
    m = sync.new_send(
        username='',
        session='',
        filename='',
        count=1,
        index=0,
        data=b'',
        length=1,
        parent_header=expected,
    )

    assert m.get_parent_header() == expected


def test_new_recv_sets_username():
    expected = 'senkwich'
    m = sync.new_recv(
        username=expected,
        session='',
        filename='',
    )

    assert m.get_header().get_username() == expected


def test_new_recv_sets_session():
    expected = 'mysession'
    m = sync.new_recv(
        username='',
        session=expected,
        filename='',
    )

    assert m.get_header().get_session() == expected


def test_new_recv_sets_filename():
    expected = 'my file'
    m = sync.new_recv(
        username='',
        session='',
        filename=expected,
    )

    assert m.get_metadata().get_value(sync.SYNC_METADATA_FILENAME) == expected


def test_new_recv_sets_parent_header():
    expected = Header.empty()
    m = sync.new_recv(
        username='',
        session='',
        filename='',
        parent_header=expected,
    )

    assert m.get_parent_header() == expected


def test_is_match_sync():
    m = Packet().set_header(Header().set_type(sync.MESSAGE_TYPE))
    assert sync.is_match(m)


def test_is_match_not_sync():
    m = Packet().set_header(Header().set_type('SOME_OTHER_TYPE'))
    assert not sync.is_match(m)


def test_is_direction_send_for_send():
    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_DIRECTION, sync.SYNC_METADATA_DIRECTION_SEND))
    assert sync.is_direction_send(m)


def test_is_direction_send_for_recv():
    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_DIRECTION, sync.SYNC_METADATA_DIRECTION_RECV))
    assert not sync.is_direction_send(m)


def test_is_direction_send_for_nothing():
    m = Packet().set_metadata(Metadata())
    assert not sync.is_direction_send(m)


def test_is_direction_recv_for_recv():
    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_DIRECTION, sync.SYNC_METADATA_DIRECTION_RECV))
    assert sync.is_direction_recv(m)


def test_is_direction_recv_for_send():
    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_DIRECTION, sync.SYNC_METADATA_DIRECTION_SEND))
    assert not sync.is_direction_recv(m)


def test_is_direction_recv_for_nothing():
    m = Packet().set_metadata(Metadata())
    assert not sync.is_direction_recv(m)


def test_get_chunk_size_for_value():
    expected = 999

    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_CHUNK_SIZE, expected))
    actual = sync.get_chunk_size(m)

    assert actual == expected


def test_get_chunk_size_for_nothing():
    expected = None

    m = Packet().set_metadata(Metadata())
    actual = sync.get_chunk_size(m)

    assert actual == expected


def test_get_chunk_count_for_value():
    expected = 999

    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_CHUNK_COUNT, expected))
    actual = sync.get_chunk_count(m)

    assert actual == expected


def test_get_chunk_count_for_nothing():
    expected = None

    m = Packet().set_metadata(Metadata())
    actual = sync.get_chunk_count(m)

    assert actual == expected


def test_get_chunk_index_for_value():
    expected = 999

    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_CHUNK_INDEX, expected))
    actual = sync.get_chunk_index(m)

    assert actual == expected


def test_get_chunk_index_for_nothing():
    expected = None

    m = Packet().set_metadata(Metadata())
    actual = sync.get_chunk_index(m)

    assert actual == expected


def test_get_filename_for_value():
    expected = 'some file name'

    m = Packet().set_metadata(Metadata().set_value(
        sync.SYNC_METADATA_FILENAME, expected))
    actual = sync.get_filename(m)

    assert actual == expected


def test_get_filename_for_nothing():
    expected = None

    m = Packet().set_metadata(Metadata())
    actual = sync.get_filename(m)

    assert actual == expected


def test_get_data_for_value():
    expected = b'some content bytes'

    m = Packet().set_content(Content().set_data(expected))
    actual = sync.get_data(m)

    assert actual == expected


def test_get_data_for_nothing():
    expected = None

    m = Packet().set_content(Content())
    actual = sync.get_data(m)

    assert actual == expected
