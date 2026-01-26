"""
Unit Tests for Text Processor Service
Tests text normalization and word splitting
"""

import pytest
from services.text_processor import TextProcessor


class TestTextProcessor:
    """Test suite for Text Processor"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.processor = TextProcessor()
    
    def test_normalize_basic(self):
        """Test basic text normalization"""
        text = "Hello world"
        result = self.processor.normalize(text)
        assert result == "Hello world"
    
    def test_normalize_extra_whitespace(self):
        """Test removal of extra whitespace"""
        text = "Hello    world"
        result = self.processor.normalize(text)
        assert "    " not in result
        assert result == "Hello world"
    
    def test_normalize_leading_trailing_whitespace(self):
        """Test removal of leading/trailing whitespace"""
        text = "   Hello world   "
        result = self.processor.normalize(text)
        assert result == "Hello world"
    
    def test_normalize_newlines(self):
        """Test conversion of newlines to spaces"""
        text = "Hello\nworld"
        result = self.processor.normalize(text)
        assert "\n" not in result
        assert "Hello" in result and "world" in result
    
    def test_normalize_punctuation_spacing(self):
        """Test fixing punctuation spacing"""
        text = "Hello.World"
        result = self.processor.normalize(text)
        assert result == "Hello.   World"
    
    def test_normalize_sentence_pauses(self):
        """Test adding pauses after sentences"""
        text = "Hello. World"
        result = self.processor.normalize(text)
        # Should have extra spaces after period
        assert ".  " in result
    
    def test_normalize_empty_string(self):
        """Test handling of empty string"""
        result = self.processor.normalize("")
        assert result == ""
    
    def test_split_words_basic(self):
        """Test basic word splitting"""
        text = "Hello world"
        result = self.processor.split_words(text)
        assert result == ["Hello", "world"]
    
    def test_split_words_multiple_spaces(self):
        """Test splitting with multiple spaces"""
        text = "Hello    world"
        result = self.processor.split_words(text)
        assert result == ["Hello", "world"]
    
    def test_split_words_empty(self):
        """Test splitting empty string"""
        result = self.processor.split_words("")
        assert result == []
    
    def test_split_words_single_word(self):
        """Test splitting single word"""
        result = self.processor.split_words("Hello")
        assert result == ["Hello"]
    
    def test_count_words(self):
        """Test word counting"""
        text = "Hello world, this is a test"
        count = self.processor.count_words(text)
        assert count == 6
    
    def test_count_sentences(self):
        """Test sentence counting"""
        text = "Hello world. This is a test. How are you?"
        count = self.processor.count_sentences(text)
        assert count >= 2  # At least 2 sentences
    
    def test_clean_punctuation(self):
        """Test punctuation cleaning"""
        assert self.processor.clean_punctuation("hello,") == "hello"
        assert self.processor.clean_punctuation("(world)") == "world"
        assert self.processor.clean_punctuation("don't") == "don't"  # Keep internal apostrophe
    
    def test_full_pipeline(self):
        """Test complete text processing pipeline"""
        text = "  Hello   world.This is   a test.  "
        normalized = self.processor.normalize(text)
        words = self.processor.split_words(normalized)
        
        assert len(words) > 0
        assert "Hello" in words
        assert "test" in words or "test." in words
    
    def test_split_multi_hyphenated_words_basic(self):
        """Test splitting words with 2+ hyphens"""
        text = "whatever-you-say-it-is"
        result = self.processor.split_words(text)
        # Should split into: ["whatever-you", "say-it", "is"]
        assert len(result) == 3
        assert "whatever-you" in result
        assert "say-it" in result
        assert "is" in result
    
    def test_split_multi_hyphenated_words_four_hyphens(self):
        """Test splitting words with 4 hyphens"""
        text = "one-two-three-four-five"
        result = self.processor.split_words(text)
        # Should split into pairs: ["one-two", "three-four", "five"]
        assert len(result) == 3
        assert "one-two" in result
        assert "three-four" in result
        assert "five" in result
    
    def test_split_single_hyphen_unchanged(self):
        """Test that words with single hyphen remain unchanged"""
        text = "well-known"
        result = self.processor.split_words(text)
        assert result == ["well-known"]
    
    def test_split_no_hyphen_unchanged(self):
        """Test that words without hyphens remain unchanged"""
        text = "hello world"
        result = self.processor.split_words(text)
        assert result == ["hello", "world"]
    
    def test_split_mixed_hyphenated_words(self):
        """Test text with mixed hyphenation"""
        text = "The state-of-the-art technology is well-known today"
        result = self.processor.split_words(text)
        # "state-of-the-art" (3 hyphens) should split to ["state-of", "the-art"]
        # "well-known" (1 hyphen) should stay as ["well-known"]
        assert "The" in result
        assert "state-of" in result
        assert "the-art" in result
        assert "technology" in result
        assert "is" in result
        assert "well-known" in result
        assert "today" in result


# Run tests with: pytest tests/test_text_processor.py -v
