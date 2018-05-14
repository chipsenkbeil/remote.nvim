# =============================================================================
# FILE: constants.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================

###############################################################################
# GENERAL CONSTANTS
###############################################################################

# Represents overall packet api version
PACKET_API_VERSION = '0.1'

###############################################################################
# PACKET TYPE HELPERS
###############################################################################

_BROADCAST_SUFFIX = '_BROADCAST'
_REQUEST_SUFFIX = '_REQUEST'
_RESPONSE_SUFFIX = '_RESPONSE'


def _broadcast(text): return text + _BROADCAST_SUFFIX


def _request(text): return text + _REQUEST_SUFFIX


def _response(text): return text + _RESPONSE_SUFFIX


# True if packet type represents a packet with no response expected
def is_broadcast(packet_type): return packet_type.endswith(_BROADCAST_SUFFIX)


# True if packet type represents a packet expecting a response
def is_request(packet_type): return packet_type.endswith(_REQUEST_SUFFIX)


# True if packet type represents a response to a packet expecting a response
def is_response(packet_type): return packet_type.endswith(_RESPONSE_SUFFIX)


###############################################################################
# PACKET TYPE CONSTANTS
###############################################################################

PACKET_TYPE_BROADCAST_ERROR = _broadcast('ERROR')
PACKET_TYPE_BROADCAST_FILE_CHANGED = _broadcast('FILE_CHANGED')
PACKET_TYPE_BROADCAST_HEARTBEAT = _broadcast('HEARTBEAT')

PACKET_TYPE_REQUEST_COMMAND = _request('COMMAND')
PACKET_TYPE_REQUEST_FILE_LIST = _request('FILE_LIST')

PACKET_TYPE_RESPONSE_COMMAND = _response('COMMAND')
PACKET_TYPE_RESPONSE_ERROR = _response('ERROR')
PACKET_TYPE_RESPONSE_FILE_LIST = _response('FILE_LIST')

PACKET_TYPE_RETRIEVE_FILE_REQUEST = 'RETRIEVE_FILE'
PACKET_TYPE_RETRIEVE_FILE = 'RETRIEVE_FILE'
PACKET_TYPE_UPDATE_FILE_START = 'UPDATE_FILE_START'
PACKET_TYPE_UPDATE_FILE_START = 'UPDATE_FILE_START'
PACKET_TYPE_UPDATE_FILE_DATA = 'UPDATE_FILE_DATA'
PACKET_TYPE_UPDATE_FILE_DATA = 'UPDATE_FILE_DATA'

###############################################################################
# BASE CONSTANTS
###############################################################################

MESSAGE_DEFAULT_USERNAME = '<UNKNOWN>'
MESSAGE_DEFAULT_SESSION = '<UNKNOWN>'

###############################################################################
# COMMAND CONSTANTS
###############################################################################

# Defaults for non-provided data
MESSAGE_DEFAULT_COMMAND_NAME = '<NAME>'
MESSAGE_DEFAULT_COMMAND_ARGS = '<ARGS>'

###############################################################################
# ERROR CONSTANTS
###############################################################################

# Defaults for non-provided data
MESSAGE_DEFAULT_ERROR_TEXT = '<ERROR>'

###############################################################################
# FILE CONSTANTS
###############################################################################

# Common metadata across file information
MESSAGE_METADATA_FILE_VERSION = 'V'

# Represents file retrieval/update metadata
MESSAGE_METADATA_FILE_LENGTH = 'L'
MESSAGE_METADATA_TOTAL_CHUNKS = 'T'
MESSAGE_METADATA_CHUNK_INDEX = 'I'

# Defaults for not-provided data
MESSAGE_DEFAULT_FILE_PATH = ''
MESSAGE_DEFAULT_FILE_LIST = []
MESSAGE_DEFAULT_FILE_LENGTH = -1
MESSAGE_DEFAULT_FILE_VERSION = 0
MESSAGE_DEFAULT_TOTAL_CHUNKS = 1
MESSAGE_DEFAULT_CHUNK_INDEX = 0
MESSAGE_DEFAULT_CHUNK_DATA = b''
MESSAGE_DEFAULT_CHUNKS_RECEIVED = 0
