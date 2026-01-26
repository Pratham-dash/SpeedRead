

from typing import Dict


class ORPCalculator:
    
    def __init__(self):
        # Future: Load exception words from database
        self.exception_words = {}  # Placeholder for future DB integration
    
    def calculate(self, word: str) -> int:
        # Future: Check exception words database first
        # if word.lower() in self.exception_words:
        #     return self.exception_words[word.lower()]
        
        length = len(word)
        
        # Calculate ORP based on word length
        if length == 1:
            return 1
        elif 2 <= length <= 5:
            return 2
        elif 6 <= length <= 9:
            return 3
        elif 10 <= length <= 13:
            return 4
        else:  # 14+ characters
            return 5
    
    def split_word(self, word: str) -> Dict[str, any]:
        # Handle empty or whitespace-only words
        if not word or not word.strip():
            return {
                'before': '',
                'orp': '',
                'after': '',
                'orp_position': 0
            }
        
        # Calculate ORP position
        orp_position = self.calculate(word)
        
        # Handle edge case: ORP position beyond word length
        # (shouldn't happen with current logic, but defensive programming)
        if orp_position > len(word):
            orp_position = len(word)
        
        # Split word at ORP position (convert to 0-indexed)
        orp_index = orp_position - 1
        
        return {
            'before': word[:orp_index],
            'orp': word[orp_index] if orp_index < len(word) else '',
            'after': word[orp_index + 1:],
            'orp_position': orp_position
        }
    
    def batch_calculate(self, words: list) -> list:
        return [self.split_word(word) for word in words]
    
    def add_exception_word(self, word: str, orp_position: int):
        # Future: Save to database
        # For now, just store in memory
        self.exception_words[word.lower()] = orp_position
    
    def get_orp_percentage(self, word: str) -> float:
        if not word:
            return 0.0
        
        orp_position = self.calculate(word)
        return orp_position / len(word)


# Module-level convenience function
def calculate_orp(word: str) -> int:
    calculator = ORPCalculator()
    return calculator.calculate(word)
