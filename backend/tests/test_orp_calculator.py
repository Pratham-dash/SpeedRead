"""
Unit Tests for ORP Calculator Service
Tests the core ORP calculation logic
"""

import pytest
from services.orp_calculator import ORPCalculator


class TestORPCalculator:
    """Test suite for ORP Calculator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.calculator = ORPCalculator()
    
    def test_single_character_word(self):
        """Test ORP for single character words"""
        assert self.calculator.calculate("I") == 1
        assert self.calculator.calculate("a") == 1
    
    def test_short_words_2_to_5_chars(self):
        """Test ORP for words with 2-5 characters"""
        assert self.calculator.calculate("is") == 2
        assert self.calculator.calculate("the") == 2
        assert self.calculator.calculate("word") == 2
        assert self.calculator.calculate("hello") == 2
    
    def test_medium_words_6_to_9_chars(self):
        """Test ORP for words with 6-9 characters"""
        assert self.calculator.calculate("reading") == 3
        assert self.calculator.calculate("computer") == 3
        assert self.calculator.calculate("beautiful") == 3
    
    def test_long_words_10_to_13_chars(self):
        """Test ORP for words with 10-13 characters"""
        assert self.calculator.calculate("programming") == 4
        assert self.calculator.calculate("information") == 4
        assert self.calculator.calculate("considerable") == 4
    
    def test_very_long_words_14_plus_chars(self):
        """Test ORP for words with 14+ characters"""
        assert self.calculator.calculate("extraordinarily") == 5
        assert self.calculator.calculate("responsibilities") == 5
    
    def test_split_word_basic(self):
        """Test word splitting at ORP"""
        result = self.calculator.split_word("reading")
        assert result['before'] == "re"
        assert result['orp'] == "a"
        assert result['after'] == "ding"
        assert result['orp_position'] == 3
    
    def test_split_word_short(self):
        """Test splitting short words"""
        result = self.calculator.split_word("the")
        assert result['before'] == "t"
        assert result['orp'] == "h"
        assert result['after'] == "e"
        assert result['orp_position'] == 2
    
    def test_split_word_single_char(self):
        """Test splitting single character"""
        result = self.calculator.split_word("I")
        assert result['before'] == ""
        assert result['orp'] == "I"
        assert result['after'] == ""
        assert result['orp_position'] == 1
    
    def test_split_word_empty(self):
        """Test handling of empty string"""
        result = self.calculator.split_word("")
        assert result['before'] == ""
        assert result['orp'] == ""
        assert result['after'] == ""
        assert result['orp_position'] == 0
    
    def test_split_word_whitespace(self):
        """Test handling of whitespace only"""
        result = self.calculator.split_word("   ")
        assert result['before'] == ""
        assert result['orp'] == ""
        assert result['after'] == ""
        assert result['orp_position'] == 0
    
    def test_batch_calculate(self):
        """Test batch ORP calculation"""
        words = ["hello", "world", "speed", "reading"]
        results = self.calculator.batch_calculate(words)
        
        assert len(results) == 4
        assert results[0]['word'] == "hello"
        assert results[0]['orp_position'] == 2
        assert results[2]['word'] == "speed"
        assert results[2]['orp_position'] == 2
    
    def test_add_exception_word(self):
        """Test adding exception words"""
        self.calculator.add_exception_word("github", 4)
        assert self.calculator.exception_words.get("github") == 4
        
        # Verify exception is used
        assert self.calculator.calculate("github") == 4
    
    def test_get_orp_percentage(self):
        """Test ORP percentage calculation"""
        percentage = self.calculator.get_orp_percentage("reading")
        assert 0.4 < percentage < 0.45  # ~43%
        
        percentage = self.calculator.get_orp_percentage("the")
        assert 0.6 < percentage < 0.7  # ~67%
    
    def test_case_insensitivity(self):
        """Test that calculation is case-insensitive"""
        assert self.calculator.calculate("HELLO") == self.calculator.calculate("hello")
        assert self.calculator.calculate("Reading") == self.calculator.calculate("reading")


# Run tests with: pytest tests/test_orp_calculator.py -v
