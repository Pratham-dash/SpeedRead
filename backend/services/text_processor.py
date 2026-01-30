

import re
from typing import List, Tuple


class TextProcessor:
    
    def is_likely_heading(self, text: str) -> bool:
        """
        Detect if text is likely a heading/title based on formatting patterns.
        Headings are:
        - All caps (e.g., "CHAPTER ONE")
        - Lines without full stop/period (e.g., "Getting Started", "Introduction")
        """
        if not text or not text.strip():
            return False
        
        text = text.strip()
        
        # Fast reject: Lines longer than 80 chars are likely paragraphs, not headings
        if len(text) > 80:
            return False
        
        # Fast path: Check for period first (most common case)
        # If it has a period, it's likely not a heading
        if '.' in text:
            # Exception: All caps text might still be a heading even with periods
            if not text.isupper():
                return False
        
        # Check 1: All caps (at least 2 words or 8+ chars)
        if text.isupper() and (len(text.split()) >= 2 or len(text) >= 8):
            return True
        
        # Check 2: Line without period and has capitalization
        if not text.endswith('.'):
            # Exclude lines ending with other sentence punctuation (!, ?, ,)
            if any(text.endswith(p) for p in ['!', '?', ',']):
                return False

            # Treat short, capitalized lines as headings. This avoids
            # misclassifying paragraph lines that were wrapped with a
            # newline (e.g., text split mid-sentence) as headings.
            words = text.split()
            if text[0].isupper() and len(words) <= 6:
                return True
        
        return False
    
    def normalize(self, text: str) -> str:
        if not text:
            return ""
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')  # Smart quotes to straight
        text = text.replace(''', "'").replace(''', "'")  # Smart single quotes
        
        # Normalize ellipsis - convert spaced periods to single ellipsis
        text = re.sub(r'\.\s*\.\s*\.', '…', text)  # . . . or ... to …
        
        # Normalize dashes - convert em/en dashes to hyphens with spaces
        text = text.replace('—', ' - ').replace('–', ' - ')
        
        # Replace multiple spaces/tabs with single space
        text = re.sub(r'[\s\t]+', ' ', text)
        
        # Replace newlines with spaces
        text = re.sub(r'\n+', ' ', text)
        
        # Fix punctuation spacing - ensure space after punctuation
        text = re.sub(r'\.(?=\S)', '. ', text)   # Space after period
        text = re.sub(r'\?(?=\S)', '? ', text)   # Space after question mark
        text = re.sub(r'!(?=\S)', '! ', text)    # Space after exclamation
        text = re.sub(r'\:(?=\S)', ': ', text)   # Space after colon
        text = re.sub(r'\;(?=\S)', '; ', text)   # Space after semicolon
        text = re.sub(r'\,(?=\S)', ', ', text)   # Space after comma
        
        # Add extra spaces after sentence endings for pause effect
        text = re.sub(r'\.\s', '.   ', text)     # 3 spaces after period
        text = re.sub(r'\?\s', '?   ', text)     # 3 spaces after question
        text = re.sub(r'!\s', '!   ', text)      # 3 spaces after exclamation
        text = re.sub(r'…\s', '…   ', text)      # 3 spaces after ellipsis
        
        # Add extra spaces after colons (often section headers)
        text = re.sub(r':\s', ':   ', text)     # 3 spaces after colon
        
        # Clean up any multiple spaces that were created
        text = re.sub(r'\s{2,}', '  ', text)     # Max 2 spaces
        
        return text.strip()
    
    def split_words(self, text: str) -> List[str]:
        if not text:
            return []
        
        # Split on whitespace (handles multiple spaces)
        words = re.split(r'\s+', text)
        
        # Filter out empty strings
        words = [w for w in words if w.strip()]
        
        # Split hyphenated words with 2+ hyphens into smaller chunks
        words = self._split_multi_hyphenated_words(words)
        
        return words
    
    def split_words_with_metadata(self, text: str) -> List[Tuple[str, dict]]:
        """
        Split text into words and detect which are likely headings.
        Returns list of tuples: (word, metadata_dict)
        metadata_dict contains: {'is_heading': bool, 'is_all_caps': bool}
        """
        if not text:
            return []
        
        text = text.strip()
        
        # Detect headings BEFORE normalization (to preserve line structure)
        lines = text.split('\n')
        
        # Pre-allocate result list for better memory efficiency
        words_with_meta = []
        
        # Normalize and process in one pass
        normalized = self.normalize(text)
        all_words = self.split_words(normalized)
        
        # Build a simple line-to-heading map (avoid storing full line objects)
        line_is_heading = []
        for line in lines:
            line = line.strip()
            if line:
                # Only check non-empty lines
                line_is_heading.append(self.is_likely_heading(line))
            else:
                line_is_heading.append(False)
        
        # Match words to lines efficiently
        word_idx = 0
        for line_idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            is_heading = line_is_heading[line_idx] if line_idx < len(line_is_heading) else False
            is_all_caps = line.isupper()
            
            # Get words for this line from normalized text
            line_normalized = self.normalize(line)
            line_words = self.split_words(line_normalized)
            
            # Tag each word from this line
            for _ in line_words:
                if word_idx < len(all_words):
                    words_with_meta.append((
                        all_words[word_idx],
                        {'is_heading': is_heading, 'is_all_caps': is_all_caps}
                    ))
                    word_idx += 1
        
        # Add remaining words (if any) as non-headings
        while word_idx < len(all_words):
            words_with_meta.append((
                all_words[word_idx],
                {'is_heading': False, 'is_all_caps': False}
            ))
            word_idx += 1
        
        return words_with_meta
    
    def _split_multi_hyphenated_words(self, words: List[str]) -> List[str]:
       
        result = []
        
        for word in words:
            # Early exit check: find if there are 2+ hyphens (O(1) space)
            first_hyphen = word.find('-')
            has_multiple_hyphens = (first_hyphen != -1 and 
                                   word.find('-', first_hyphen + 1) != -1)
            
            # If word has 2+ hyphens, split it into chunks
            if has_multiple_hyphens:
                # Split on hyphens
                parts = word.split('-')
                
                # Rejoin into pairs (with single hyphen)
                for i in range(0, len(parts), 2):
                    if i + 1 < len(parts):
                        # Pair two parts with a hyphen
                        result.append(f"{parts[i]}-{parts[i+1]}")
                    else:
                        # Last part if odd number of segments
                        result.append(parts[i])
            else:
                # Keep word as is (0 or 1 hyphen)
                result.append(word)
        
        return result
    
    def remove_special_formatting(self, text: str) -> str:
       
        return text
    
    def count_words(self, text: str) -> int:
        words = self.split_words(self.normalize(text))
        return len(words)
    
    def count_sentences(self, text: str) -> int:
        # Simple sentence counting based on punctuation
        sentence_endings = len(re.findall(r'[.!?]+', text))
        return max(1, sentence_endings)  # At least 1 sentence
    
    def clean_punctuation(self, word: str) -> str:
        
        word = re.sub(r'^[^\w]+', '', word)  # Remove leading punctuation
        word = re.sub(r'[^\w]+$', '', word)  # Remove trailing punctuation
        return word
