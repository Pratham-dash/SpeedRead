

import re
from typing import Tuple, Optional
import config


class Validator:
    
    MAX_TEXT_LENGTH = config.Config.MAX_TEXT_LENGTH
    MIN_TEXT_LENGTH = config.Config.MIN_TEXT_LENGTH
    
    @staticmethod
    def validate_text_input(text: str) -> Tuple[bool, Optional[str]]:
        # Check if text is string
        if not isinstance(text, str):
            return False, "Text must be a string"
        
        # Check if empty or whitespace only
        if not text or not text.strip():
            return False, "Text cannot be empty or whitespace only"
        
        # Check minimum length
        if len(text) < Validator.MIN_TEXT_LENGTH:
            return False, f"Text too short (minimum {Validator.MIN_TEXT_LENGTH} character)"
        
        # Check maximum length
        if len(text) > Validator.MAX_TEXT_LENGTH:
            return False, f"Text too long (maximum {Validator.MAX_TEXT_LENGTH} characters)"
        
        return True, None
    
    @staticmethod
    def validate_word(word: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(word, str):
            return False, "Word must be a string"
        
        if not word or not word.strip():
            return False, "Word cannot be empty"
        
        if len(word) > 100:
            return False, "Word too long (maximum 100 characters)"
        
        return True, None
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        # URL regex pattern
        pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP address
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$',  # path
            re.IGNORECASE
        )
        return pattern.match(url) is not None
    
    @staticmethod
    def validate_wpm(wpm: int) -> Tuple[bool, Optional[str]]:
        if not isinstance(wpm, int):
            return False, "WPM must be an integer"
        
        if wpm < 100:
            return False, "WPM too low (minimum 100)"
        
        if wpm > 2000:
            return False, "WPM too high (maximum 2000)"
        
        return True, None
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: list) -> Tuple[bool, Optional[str]]:
        if not filename:
            return False, "Filename cannot be empty"
        
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        
        if not extension:
            return False, "File must have an extension"
        
        if f'.{extension}' not in allowed_extensions:
            return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        
        return True, None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        # Remove path separators
        filename = filename.replace('/', '_').replace('\\', '_')
        
        # Remove parent directory references
        filename = filename.replace('..', '')
        
        # Remove other dangerous characters
        filename = re.sub(r'[<>:"|?*]', '', filename)
        
        return filename
    
    @staticmethod
    def validate_pagination(page: int, per_page: int) -> Tuple[bool, Optional[str]]:
        if page < 1:
            return False, "Page number must be >= 1"
        
        if per_page < 1 or per_page > 1000:
            return False, "Items per page must be between 1 and 1000"
        
        return True, None
