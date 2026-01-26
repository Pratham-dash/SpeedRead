"""
Application Configuration
Loads settings from environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Flask Core Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')
    
    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')  # Restrict in production
    
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
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'False').lower() == 'true'
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    MAX_TEXT_LENGTH = 100_000  # Lower limit for testing


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
