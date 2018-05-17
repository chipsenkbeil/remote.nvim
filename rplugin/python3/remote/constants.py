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

_TELL_SUFFIX = '_TELL'
_ASK_SUFFIX = '_ASK'
_ANSWER_SUFFIX = '_ANSWER'


def _tell(text): return text + _TELL_SUFFIX


def _ask(text): return text + _ASK_SUFFIX


def _answer(text): return text + _ANSWER_SUFFIX


# True if packet type represents a packet with no answer expected
def is_tell(packet_type): return packet_type.endswith(_TELL_SUFFIX)


# True if packet type represents a packet expecting an answer
def is_ask(packet_type): return packet_type.endswith(_ASK_SUFFIX)


# True if packet type represents an answer to an ask packet
def is_answer(packet_type): return packet_type.endswith(_ANSWER_SUFFIX)


###############################################################################
# PACKET TYPE CONSTANTS
###############################################################################

PACKET_TYPE_TELL_ERROR = _tell('ERROR')
PACKET_TYPE_TELL_FILE_CHANGED = _tell('FILE_CHANGED')
PACKET_TYPE_TELL_HEARTBEAT = _tell('HEARTBEAT')

PACKET_TYPE_ASK_COMMAND = _ask('COMMAND')
PACKET_TYPE_ASK_FILE_LIST = _ask('FILE_LIST')

PACKET_TYPE_ANSWER_COMMAND = _answer('COMMAND')
PACKET_TYPE_ANSWER_ERROR = _answer('ERROR')
PACKET_TYPE_ANSWER_FILE_LIST = _answer('FILE_LIST')

PACKET_TYPE_RETRIEVE_FILE_ASK = 'RETRIEVE_FILE'
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
