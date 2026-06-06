"""
Application Configuration
Loads settings from environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _parse_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() == 'true'


def _parse_cors_origins(value: str) -> list[str]:
    """Parse comma-separated origins into a normalized allowlist."""
    if not value:
        return []

    raw_origins = [origin.strip() for origin in value.split(',') if origin.strip()]
    normalized_origins = []

    for origin in raw_origins:
        if origin == '*':
            normalized_origins.append('*')
            continue
        normalized_origins.append(origin.rstrip('/'))

    return normalized_origins


class Config:
    # Flask Core Settings
    ENV = os.getenv('FLASK_ENV', 'development').lower()
    DEBUG = _parse_bool(os.getenv('DEBUG'), default=(ENV != 'production'))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # API routing
    API_BASE_PATH = '/api'

    # CORS Settings
    # Development defaults are permissive for common local frontend ports.
    _DEFAULT_DEV_CORS = 'http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://127.0.0.1:3000'
    CORS_ORIGINS_RAW = os.getenv('CORS_ORIGINS', _DEFAULT_DEV_CORS if ENV != 'production' else '')
    CORS_ORIGINS = _parse_cors_origins(CORS_ORIGINS_RAW)

    if ENV == 'production' and not CORS_ORIGINS:
        raise ValueError(
            'CORS_ORIGINS must be set in production (comma-separated origins).'
        )

    # File Upload Limits (for future PDF support)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Text Processing Limits
    MAX_TEXT_LENGTH = 1_000_000  # 1MB text limit (1 million characters)
    MIN_TEXT_LENGTH = 1

    # Word Processing Settings
    LONG_WORD_THRESHOLD = 7  # Words longer than this get duplicated
    PAUSE_COUNT = 4  # Number of blank pauses after sentences

    # Database (Future - when implementing persistence)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///speedread.db')

    # API Keys (Future - for content extraction services)
    DIFFBOT_API_KEY = os.getenv('DIFFBOT_API_KEY', '')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Rate Limiting (Future - when implementing rate limits)
    RATELIMIT_ENABLED = _parse_bool(os.getenv('RATELIMIT_ENABLED'), default=False)
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    # Keep tests isolated from production CORS requirements
    CORS_ORIGINS = ['*']
    MAX_TEXT_LENGTH = 100_000  # Lower limit for testing


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
