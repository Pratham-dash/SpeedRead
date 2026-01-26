"""
Shared Constants
Application-wide constants and configuration values
"""

# ============================================================
# ORP CALCULATION CONSTANTS
# ============================================================

# ORP lookup table (word length → ORP position)
ORP_LOOKUP_TABLE = {
    1: 1,   # "I" → position 1
    2: 2,   # "is" → position 2
    3: 2,   # "the" → position 2
    4: 2,   # "word" → position 2
    5: 2,   # "hello" → position 2
    6: 3,   # "reading" → position 3
    7: 3,
    8: 3,
    9: 3,
    10: 4,  # "programming" → position 4
    11: 4,
    12: 4,
    13: 4,
    # 14+ → position 5
}

# Alternative ORP calculation method (percentage-based)
ORP_PERCENTAGE = 0.35  # Optimal viewing position at ~35% from start


# ============================================================
# TEXT PROCESSING CONSTANTS
# ============================================================

# Sentence ending markers
SENTENCE_ENDINGS = ['.', '!', '?', ':', ';', ')']

# Clause separators
CLAUSE_SEPARATORS = [',', ';', '—', '–']

# Quote markers
QUOTE_MARKERS = ['"', "'", '"', '"', ''', ''']

# Common stop words (for future NLP features)
STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
    'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'from',
    'and', 'or', 'but', 'not', 'so', 'as', 'if', 'than'
}


# ============================================================
# WORD PREPROCESSING CONSTANTS
# ============================================================

# Default settings for word preprocessing
DEFAULT_LONG_WORD_THRESHOLD = 7  # Words longer than this get duplicated
DEFAULT_PAUSE_COUNT = 4  # Number of blank pauses after sentences
DEFAULT_DUPLICATION_COUNT = 3  # How many times to show long words


# ============================================================
# READING SPEED CONSTANTS
# ============================================================

# Reading speed categories (words per minute)
READING_SPEEDS = {
    'beginner': 200,
    'average': 300,
    'advanced': 500,
    'expert': 800,
    'speed_reader': 1000
}

# Recommended WPM ranges
MIN_WPM = 100
MAX_WPM = 2000
DEFAULT_WPM = 300


# ============================================================
# FILE PROCESSING CONSTANTS
# ============================================================

# Supported file types (for future features)
SUPPORTED_DOCUMENT_TYPES = ['.txt', '.pdf', '.docx', '.epub']
SUPPORTED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.gif']

# File size limits (bytes)
MAX_FILE_SIZE_PDF = 16 * 1024 * 1024  # 16MB
MAX_FILE_SIZE_TEXT = 1 * 1024 * 1024  # 1MB

# PDF extraction settings
PDF_MAX_PAGES = 500  # Maximum pages to process


# ============================================================
# API CONSTANTS
# ============================================================

# API response messages
SUCCESS_MESSAGE = "Processing completed successfully"
ERROR_MESSAGE_GENERIC = "An error occurred during processing"
ERROR_MESSAGE_INVALID_INPUT = "Invalid input provided"
ERROR_MESSAGE_SERVER_ERROR = "Internal server error"

# HTTP status codes (for reference)
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500
HTTP_NOT_IMPLEMENTED = 501


# ============================================================
# VALIDATION CONSTANTS
# ============================================================

# Text input limits
MAX_TEXT_LENGTH = 1_000_000  # 1 million characters
MIN_TEXT_LENGTH = 1

# Word limits
MAX_WORD_LENGTH = 100
MIN_WORD_LENGTH = 1

# URL validation patterns
VALID_URL_SCHEMES = ['http', 'https']


# ============================================================
# EXCEPTION WORDS (Future DB Integration)
# ============================================================

# Placeholder for exception words with custom ORP positions
# Will be loaded from database in future implementation
EXCEPTION_WORDS = {
    # Example entries:
    # 'github': 4,  # Focus on 'H' in GitHub
    # 'javascript': 5,  # Custom ORP for JavaScript
}


# ============================================================
# LANGUAGE SUPPORT (Future Feature)
# ============================================================

# Supported languages (placeholder for future multi-language support)
SUPPORTED_LANGUAGES = {
    'en': 'English',
    # 'es': 'Spanish',
    # 'fr': 'French',
    # 'de': 'German',
}

DEFAULT_LANGUAGE = 'en'


# ============================================================
# CACHING CONSTANTS (Future Feature)
# ============================================================

# Cache TTL (time to live) in seconds
CACHE_TTL_SHORT = 60 * 5  # 5 minutes
CACHE_TTL_MEDIUM = 60 * 30  # 30 minutes
CACHE_TTL_LONG = 60 * 60 * 24  # 24 hours

# Cache key prefixes
CACHE_PREFIX_ORP = 'orp:'
CACHE_PREFIX_TEXT = 'text:'
CACHE_PREFIX_STATS = 'stats:'


# ============================================================
# LOGGING CONSTANTS
# ============================================================

# Log levels
LOG_LEVEL_DEBUG = 'DEBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'

# Log formats
LOG_FORMAT_SIMPLE = '%(levelname)s: %(message)s'
LOG_FORMAT_DETAILED = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
