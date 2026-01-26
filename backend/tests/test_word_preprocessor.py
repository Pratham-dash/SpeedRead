"""
Unit Tests for Word Preprocessor Service
Tests smart pacing and word duplication logic
"""

import pytest
from services.word_preprocessor import WordPreprocessor


class TestWordPreprocessor:
    """Test suite for Word Preprocessor"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.preprocessor = WordPreprocessor(long_word_threshold=7, pause_count=4)
    
    def test_preprocess_short_words(self):
        """Test that short words are not duplicated"""
        words = ["hello", "world"]
        result = self.preprocessor.preprocess(words)
        # Short words should appear once, no sentence endings so no pauses
        assert result == ["hello", "world"]
    
    def test_preprocess_long_words(self):
        """Test that long words are duplicated 3x"""
        words = ["wonderful"]  # 9 characters > 7
        result = self.preprocessor.preprocess(words)
        # Should have 3 copies
        assert result.count("wonderful") == 3
    
    def test_preprocess_with_comma(self):
        """Test that words with commas are duplicated"""
        words = ["hello,"]
        result = self.preprocessor.preprocess(words)
        # Should have 3 copies
        assert result.count("hello,") == 3
    
    def test_preprocess_sentence_endings(self):
        """Test that sentence endings add pauses"""
        words = ["hello."]
        result = self.preprocessor.preprocess(words)
        # Should have word + 4 blank pauses
        assert len(result) == 5
        assert result[0] == "hello."
        assert result[1:] == [' ', ' ', ' ', ' ']
    
    def test_preprocess_complex(self):
        """Test complex preprocessing with multiple rules"""
        words = ["Hello", "wonderful", "world."]
        result = self.preprocessor.preprocess(words)
        
        # "Hello" appears once
        assert result.count("Hello") == 1
        # "wonderful" appears 3 times (long word)
        assert result.count("wonderful") == 3
        # "world." appears once + has 4 pauses after
        assert result.count("world.") == 1
        # Check for pauses
        assert ' ' in result
    
    def test_estimate_reading_time(self):
        """Test reading time estimation"""
        # 300 words at 300 WPM should take 60 seconds
        time = self.preprocessor.estimate_reading_time(300, 300)
        assert time == 60.0
        
        # 150 words at 300 WPM should take 30 seconds
        time = self.preprocessor.estimate_reading_time(150, 300)
        assert time == 30.0
    
    def test_estimate_reading_time_edge_cases(self):
        """Test reading time with edge cases"""
        # Zero words
        time = self.preprocessor.estimate_reading_time(0, 300)
        assert time == 0.0
        
        # Zero WPM (shouldn't happen, but test anyway)
        time = self.preprocessor.estimate_reading_time(100, 0)
        assert time == 0.0
    
    def test_should_duplicate_logic(self):
        """Test duplication decision logic"""
        # Short word should not duplicate
        assert not self.preprocessor._should_duplicate("hello")
        
        # Long word should duplicate
        assert self.preprocessor._should_duplicate("wonderful")
        
        # Word with comma should duplicate
        assert self.preprocessor._should_duplicate("hello,")
    
    def test_is_sentence_ending(self):
        """Test sentence ending detection"""
        assert self.preprocessor._is_sentence_ending("hello.")
        assert self.preprocessor._is_sentence_ending("world!")
        assert self.preprocessor._is_sentence_ending("really?")
        assert not self.preprocessor._is_sentence_ending("hello")
    
    def test_get_statistics(self):
        """Test preprocessing statistics"""
        original = ["Hello", "wonderful", "world."]
        processed = self.preprocessor.preprocess(original)
        stats = self.preprocessor.get_statistics(original, processed)
        
        assert stats['original_count'] == 3
        assert stats['processed_count'] > 3  # Due to duplicates and pauses
        assert stats['duplicated_words'] >= 1  # "wonderful" is duplicated
        assert stats['sentence_endings'] >= 1  # "world." ends sentence
    
    def test_preprocess_without_pauses(self):
        """Test preprocessing without sentence pauses"""
        words = ["Hello", "world."]
        result = self.preprocessor.preprocess_without_pauses(words)
        
        # Should not have blank pauses
        assert ' ' not in result
        # Should still have the words
        assert "Hello" in result
        assert "world." in result
    
    def test_custom_threshold(self):
        """Test custom word length threshold"""
        # Create preprocessor with threshold of 5
        custom = WordPreprocessor(long_word_threshold=5, pause_count=2)
        words = ["hello"]  # 5 characters, not > 5
        result = custom.preprocess(words)
        
        # Should not be duplicated
        assert result.count("hello") == 1
        
        words = ["wonderful"]  # 9 characters > 5
        result = custom.preprocess(words)
        
        # Should be duplicated
        assert result.count("wonderful") == 3


# Run tests with: pytest tests/test_word_preprocessor.py -v
