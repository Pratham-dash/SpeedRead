"""
Exception Words Model
Placeholder for future database model storing words with custom ORP positions

Use Case:
--------
Store words that need non-standard ORP positions due to:
- Brand names: "GitHub" → Focus on 'H' instead of calculated position
- Compound words: "JavaScript" → Custom focal point
- Acronyms: "NASA" → Special handling
- User preferences: Custom ORP for specific words

Schema (Future Implementation):
-------------------------------
When database is added, this will be the model structure:

Table: exception_words
- id: Integer, Primary Key, Auto-increment
- word: String(100), Unique, Not Null, Indexed
- orp_position: Integer, Not Null (1-indexed)
- reason: String(500), Optional (why it's an exception)
- language: String(10), Default 'en'
- created_at: DateTime, Default NOW()
- updated_at: DateTime, Default NOW(), On Update NOW()
- created_by: String(100), Optional (user who added it)

Example Data:
------------
id | word       | orp_position | reason                           | language
---+------------+--------------+----------------------------------+---------
1  | github     | 4            | Focus on capital 'H'             | en
2  | javascript | 5            | Better recognition at 'S'        | en
3  | nasa       | 2            | Acronym - focus on second letter | en

Future Implementation:
---------------------
Uncomment the code below when adding database support.
Install: Flask-SQLAlchemy, Flask-Migrate

"""

# TODO: Uncomment when implementing database
# 
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# 
# db = SQLAlchemy()
# 
# 
# class ExceptionWord(db.Model):
#     """
#     Exception Words Database Model
#     Stores words with custom ORP positions that override standard calculation
#     """
#     
#     __tablename__ = 'exception_words'
#     
#     # Primary Key
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     
#     # Word Data
#     word = db.Column(
#         db.String(100),
#         unique=True,
#         nullable=False,
#         index=True,
#         comment="The word with custom ORP (lowercase)"
#     )
#     
#     # ORP Position
#     orp_position = db.Column(
#         db.Integer,
#         nullable=False,
#         comment="Custom ORP position (1-indexed)"
#     )
#     
#     # Metadata
#     reason = db.Column(
#         db.String(500),
#         nullable=True,
#         comment="Explanation for custom ORP"
#     )
#     
#     language = db.Column(
#         db.String(10),
#         default='en',
#         nullable=False,
#         index=True,
#         comment="Language code (ISO 639-1)"
#     )
#     
#     # Timestamps
#     created_at = db.Column(
#         db.DateTime,
#         default=datetime.utcnow,
#         nullable=False
#     )
#     
#     updated_at = db.Column(
#         db.DateTime,
#         default=datetime.utcnow,
#         onupdate=datetime.utcnow,
#         nullable=False
#     )
#     
#     created_by = db.Column(
#         db.String(100),
#         nullable=True,
#         comment="User who created this exception"
#     )
#     
#     def __repr__(self):
#         return f"<ExceptionWord {self.word} → position {self.orp_position}>"
#     
#     def to_dict(self):
#         """Convert model to dictionary"""
#         return {
#             'id': self.id,
#             'word': self.word,
#             'orp_position': self.orp_position,
#             'reason': self.reason,
#             'language': self.language,
#             'created_at': self.created_at.isoformat(),
#             'updated_at': self.updated_at.isoformat(),
#             'created_by': self.created_by
#         }
#     
#     @classmethod
#     def get_by_word(cls, word: str):
#         """Get exception word by word string"""
#         return cls.query.filter_by(word=word.lower()).first()
#     
#     @classmethod
#     def get_all_for_language(cls, language: str = 'en'):
#         """Get all exception words for a language"""
#         return cls.query.filter_by(language=language).all()
#     
#     @classmethod
#     def create_exception(cls, word: str, orp_position: int, reason: str = None, language: str = 'en'):
#         """Create a new exception word"""
#         exception = cls(
#             word=word.lower(),
#             orp_position=orp_position,
#             reason=reason,
#             language=language
#         )
#         db.session.add(exception)
#         db.session.commit()
#         return exception


# Migration Commands (Future):
# ---------------------------
# flask db init
# flask db migrate -m "Create exception_words table"
# flask db upgrade


# Example Usage (Future):
# -----------------------
# from models.exception_words import ExceptionWord, db
# 
# # Create exception
# ExceptionWord.create_exception(
#     word="github",
#     orp_position=4,
#     reason="Focus on capital H for better brand recognition"
# )
# 
# # Query exception
# exception = ExceptionWord.get_by_word("github")
# if exception:
#     print(f"Custom ORP for {exception.word}: {exception.orp_position}")
# 
# # Get all exceptions
# all_exceptions = ExceptionWord.get_all_for_language('en')
