

from typing import List, Tuple
import config


class WordPreprocessor:
    
    def __init__(self, long_word_threshold: int = None, pause_count: int = None):
        self.long_word_threshold = long_word_threshold or config.Config.LONG_WORD_THRESHOLD
        self.pause_count = pause_count or config.Config.PAUSE_COUNT
    
    def preprocess(self, words: List[str]) -> List[str]:
        processed = []
        
        for word in words:
            # Add the original word
            processed.append(word)
            
            # Rule 1: Duplicate long words (more processing time needed)
            # Rule 2: Duplicate words with commas (pause needed)
            if self._should_duplicate(word):
                # Add 2 more copies (total of 3 appearances)
                processed.extend([word, word])
            
            # Rule 3: Add blank pauses after sentence endings
            if self._is_sentence_ending(word):
                # Add blank pauses for comprehension break
                processed.extend([' '] * self.pause_count)
        
        return processed
    
    def preprocess_with_headings(self, words_with_meta: List[Tuple[str, dict]]) -> List[dict]:
        """
        Enhanced preprocessing that handles headings with extra pauses and slower display.
        Takes list of (word, metadata) tuples and returns list of word dictionaries.
        
        Returns list of dicts with:
        - word: str
        - is_heading: bool
        - display_multiplier: int (how many times to show the word)
        """
        processed = []
        heading_words = []
        in_heading = False
        
        for i, (word, meta) in enumerate(words_with_meta):
            is_heading = meta.get('is_heading', False)
            is_all_caps = meta.get('is_all_caps', False)
            
            # Track heading start/end
            if is_heading and not in_heading:
                # Starting a new heading - add pause before
                for _ in range(self.pause_count):
                    processed.append({
                        'word': ' ',
                        'is_heading': False,
                        'display_multiplier': 1
                    })
                in_heading = True
                heading_words = []
            
            # Determine display multiplier
            if is_heading or is_all_caps:
                # Headings and all-caps: show 4-5 times (much slower)
                multiplier = 3
            elif self._should_duplicate(word):
                # Long words or comma words: show 3 times
                multiplier = 3
            else:
                # Normal words: show once
                multiplier = 1
            
            # Add the word
            processed.append({
                'word': word,
                'is_heading': is_heading,
                'display_multiplier': multiplier
            })
            
            # Add sentence ending pauses
            if self._is_sentence_ending(word) and not is_heading:
                for _ in range(self.pause_count):
                    processed.append({
                        'word': ' ',
                        'is_heading': False,
                        'display_multiplier': 1
                    })
            
            # Check if heading is ending
            if in_heading:
                heading_words.append(word)
                # Heading ends if next word is not a heading
                next_is_heading = False
                if i + 1 < len(words_with_meta):
                    next_is_heading = words_with_meta[i + 1][1].get('is_heading', False)
                
                if not next_is_heading:
                    # End of heading - add 5 blank pauses
                    for _ in range(5):
                        processed.append({
                            'word': ' ',
                            'is_heading': False,
                            'display_multiplier': 1
                        })
                    in_heading = False
        
        return processed
    
    def _should_duplicate(self, word: str) -> bool:
        # Check length (excluding punctuation for fair comparison)
        clean_word = word.strip('.,!?;:()[]{}"\'-')
        is_long = len(clean_word) > self.long_word_threshold
        
        # Check for comma (indicates clause break)
        has_comma = ',' in word
        
        return is_long or has_comma
    
    def _is_sentence_ending(self, word: str) -> bool:
        sentence_markers = ['.', '!', '?', ':', ';', ')']
        return any(marker in word for marker in sentence_markers)
    
    def estimate_reading_time(self, word_count: int, wpm: int = 300) -> float:
        if word_count <= 0 or wpm <= 0:
            return 0.0
        
        return (word_count / wpm) * 60
    
    def get_statistics(self, original_words: List[str], processed_words: List[str]) -> dict:
        duplicated_count = sum(1 for w in original_words if self._should_duplicate(w))
        pause_count = sum(1 for w in original_words if self._is_sentence_ending(w))
        
        return {
            'original_count': len(original_words),
            'processed_count': len(processed_words),
            'duplicated_words': duplicated_count,
            'sentence_endings': pause_count,
            'total_pauses': pause_count * self.pause_count,
            'expansion_ratio': len(processed_words) / len(original_words) if original_words else 1.0
        }
    
    def preprocess_without_pauses(self, words: List[str]) -> List[str]:
        processed = []
        
        for word in words:
            processed.append(word)
            
            if self._should_duplicate(word):
                processed.extend([word, word])
        
        return processed
    
    def customize_duplication(self, words: List[str], duplication_map: dict) -> List[str]:
        processed = []
        
        for word in words:
            # Get custom duplication count or default to 1
            count = duplication_map.get(word.lower(), 1)
            processed.extend([word] * count)
        
        return processed
