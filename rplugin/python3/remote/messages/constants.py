# =============================================================================
# FILE: constants.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.cop>
# License: Apache 2.0 License
# =============================================================================

###############################################################################
# GENERAL CONSTANTS
###############################################################################

# Represents overall message api version
MESSAGE_API_VERSION = '0.1'

###############################################################################
# MESSAGE TYPE CONSTANTS
###############################################################################

# Represents the types of messages request/response/broadcast
MESSAGE_TYPE_COMMAND = 'COMMAND'
MESSAGE_TYPE_ERROR = 'ERROR'
MESSAGE_TYPE_FILE_CHANGED = 'FILE_CHANGED'
MESSAGE_TYPE_FILE_LIST = 'FILE_LIST'
MESSAGE_TYPE_RETRIEVE_FILE = 'RETRIEVE_FILE'
MESSAGE_TYPE_UPDATE_FILE_START = 'UPDATE_FILE_START'
MESSAGE_TYPE_UPDATE_FILE_DATA = 'UPDATE_FILE_DATA'

# Represents the subtype this message represents
MESSAGE_SUBTYPE = 'SUBTYPE'
MESSAGE_SUBTYPE_REQUEST = 'REQUEST'
MESSAGE_SUBTYPE_RESPONSE = 'RESPONSE'
MESSAGE_SUBTYPE_BROADCAST = 'BROADCAST'

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
