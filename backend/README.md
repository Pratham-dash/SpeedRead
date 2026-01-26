# SpeedRead Backend API

Flask-based REST API for speed reading text processing with Optimal Recognition Point (ORP) calculation.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Configuration](#configuration)
- [Development](#development)

## ✨ Features

- **ORP Calculation**: Scientifically-optimized focal point for each word
- **Smart Text Processing**: Normalization, word splitting, and preprocessing
- **Word Pacing**: Intelligent duplication and pausing for better comprehension
- **Modular Architecture**: Clean separation of concerns (API → Services → Utils)
- **Comprehensive Validation**: Input validation with detailed error messages
- **Future-Ready**: Placeholders for PDF extraction and URL scraping
- **Full Test Coverage**: Unit and integration tests

## 🏗️ Architecture

```
backend/
├── api/                    # API Layer (HTTP endpoints)
│   ├── routes.py          # Route definitions and request handling
│   ├── schemas.py         # Pydantic validation models
│   └── error_handlers.py  # Global error handlers
├── services/              # Business Logic Layer
│   ├── text_processor.py        # Text normalization and splitting
│   ├── orp_calculator.py        # ORP calculation logic
│   ├── word_preprocessor.py     # Smart pacing and duplication
│   └── content_extractor.py     # Content extraction orchestration
├── utils/                 # Utility Layer
│   ├── validators.py      # Input validation functions
│   ├── constants.py       # Application constants
│   ├── pdf_extractor.py   # PDF extraction (placeholder)
│   └── url_scraper.py     # URL scraping (placeholder)
├── models/                # Data Models (future database)
│   └── exception_words.py # Custom ORP exceptions model
└── tests/                 # Test Suite
    ├── test_orp_calculator.py
    ├── test_text_processor.py
    ├── test_word_preprocessor.py
    └── test_api.py
```

### Layer Separation Rules

- **API Layer**: Only handles HTTP requests/responses, delegates to services
- **Services Layer**: Contains business logic, no HTTP awareness
- **Utils Layer**: Pure functions, no state, reusable across services
- **No Cross-Dependencies**: Services don't import from API, Utils don't import from Services

## 🚀 Setup

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Installation

1. **Clone repository** (if not already done)
   ```bash
   cd /home/pratham_dash/SpeedRead/backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Linux/Mac
   source venv/bin/activate
   
   # Windows (if running locally)
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run the application**
   ```bash
   # Development mode
   python app.py
   
   # Production mode (with Gunicorn)
   gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
   ```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "SpeedRead API",
  "version": "1.0.0"
}
```

---

### Process Text

**POST** `/api/process-text`

Process text for speed reading with ORP calculation.

**Request:**
```json
{
  "text": "Hello world. This is a test.",
  "duplicate_long_words": true,
  "add_sentence_pauses": true
}
```

**Parameters:**
- `text` (string, required): Text to process (1 to 1,000,000 characters)
- `duplicate_long_words` (boolean, optional): Duplicate long words 3x for better focus (default: true)
- `add_sentence_pauses` (boolean, optional): Add pauses after sentences (default: true)

**Response:**
```json
{
  "success": true,
  "words": ["Hello", "world.", " ", " ", " ", " ", "This", "is", "a", "test."],
  "orp_data": [
    {
      "word": "Hello",
      "before": "He",
      "orp": "l",
      "after": "lo",
      "orp_position": 3
    }
  ],
  "stats": {
    "word_count": 5,
    "processed_count": 10,
    "sentence_count": 2,
    "estimated_time_seconds": 2.0
  },
  "analysis": {
    "recommendation": "Use Backend ORP",
    "reasons": [
      "Future extensibility for custom exception words",
      "Centralized updates without frontend redeployment"
    ]
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (empty text, too long, etc.)
- `500 Internal Server Error`: Processing error

---

### Calculate ORP

**POST** `/api/calculate-orp`

Calculate ORP for a single word.

**Request:**
```json
{
  "word": "reading"
}
```

**Response:**
```json
{
  "success": true,
  "word": "reading",
  "before": "re",
  "orp": "a",
  "after": "ding",
  "orp_position": 3,
  "word_length": 7,
  "orp_percentage": 42.86
}
```

---

### Test Endpoint

**GET** `/api/test`

Simple test endpoint to verify API connectivity.

**Response:**
```json
{
  "message": "SpeedRead API is working!",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### Future Endpoints (Not Implemented)

#### Extract from URL

**POST** `/api/extract-url`

Extract text content from a URL (Coming Soon).

**Request:**
```json
{
  "url": "https://example.com/article"
}
```

**Current Response:** `501 Not Implemented`

---

#### Upload PDF

**POST** `/api/upload-pdf`

Extract text from uploaded PDF (Coming Soon).

**Request:** `multipart/form-data` with PDF file

**Current Response:** `501 Not Implemented`

---

## 🧪 Testing

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_orp_calculator.py -v
```

### Test Structure

- **test_orp_calculator.py**: ORP calculation logic
  - Single character words (1 → position 1)
  - Short words 2-5 chars (→ position 2)
  - Medium words 6-9 chars (→ position 3)
  - Long words 10-13 chars (→ position 4)
  - Very long words 14+ chars (→ position 5)
  - Word splitting at ORP
  - Exception words
  - Batch processing

- **test_text_processor.py**: Text normalization
  - Whitespace normalization
  - Punctuation spacing
  - Sentence pause insertion
  - Word splitting and counting

- **test_word_preprocessor.py**: Smart pacing
  - Long word duplication (3x)
  - Comma-ending duplication
  - Sentence ending pauses
  - Reading time estimation

- **test_api.py**: Integration tests
  - All endpoint responses
  - Error handling (400, 404, 405, 501)
  - Request validation
  - JSON parsing

### Expected Test Results

All tests should pass:
```
tests/test_api.py ...................... [ 40%]
tests/test_orp_calculator.py ........... [ 65%]
tests/test_text_processor.py ........... [ 85%]
tests/test_word_preprocessor.py ........ [100%]

============ 45 passed in 2.34s ============
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Flask Configuration
FLASK_ENV=development          # development or production
SECRET_KEY=your-secret-key-here
DEBUG=True                     # Set to False in production

# CORS Configuration
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Text Processing
MAX_TEXT_LENGTH=1000000        # Maximum text length in characters
LONG_WORD_THRESHOLD=7          # Characters to consider "long word"
PAUSE_COUNT=4                  # Number of blank pauses after sentences

# Future Features (placeholders)
# DATABASE_URL=sqlite:///speedread.db
# PDF_EXTRACT_ENABLED=false
# URL_SCRAPE_ENABLED=false
```

### ORP Calculation Rules

The ORP (Optimal Recognition Point) is calculated based on word length:

| Word Length | ORP Position | Example |
|-------------|--------------|---------|
| 1 character | Position 1 | **I** |
| 2-5 characters | Position 2 | t**h**e, wo**r**ld |
| 6-9 characters | Position 3 | re**a**ding |
| 10-13 characters | Position 4 | pro**g**ramming |
| 14+ characters | Position 5 | extr**a**ordinarily |

These positions are based on eye-tracking research showing where readers naturally fixate for optimal word recognition.

## 🛠️ Development

### Adding New Features

1. **Add constants** to `utils/constants.py`
2. **Create utility functions** in `utils/` (pure functions)
3. **Implement service logic** in `services/` (business logic)
4. **Add API endpoint** in `api/routes.py` (HTTP layer)
5. **Add validation schema** to `api/schemas.py`
6. **Write tests** in `tests/`

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions small and focused (single responsibility)

### Running in Development

```bash
# Enable debug mode and auto-reload
export FLASK_ENV=development
export DEBUG=True
python app.py
```

### Common Development Tasks

```bash
# Install new package
pip install package-name
pip freeze > requirements.txt

# Run specific test
pytest tests/test_orp_calculator.py::TestORPCalculator::test_single_character_word -v

# Check code style
flake8 . --exclude=venv --max-line-length=100

# Format code
black . --exclude=venv
```

## 🔮 Future Features

### Coming Soon

- **PDF Text Extraction**: Upload PDFs and extract readable text
- **URL Content Scraping**: Extract article content from web pages
- **Custom Exception Words**: Database of words with custom ORP positions
- **User Preferences**: Save reading speed, theme preferences
- **Reading Statistics**: Track words read, time spent, progress over time
- **Multiple Languages**: Support for non-English texts with different ORP rules

### Implementing PDF Extraction

Update `utils/pdf_extractor.py`:

```python
# Install: pip install PyPDF2
import PyPDF2

class PDFExtractor:
    def extract_text(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
```

### Implementing URL Scraping

Update `utils/url_scraper.py`:

```python
# Install: pip install beautifulsoup4 requests
from bs4 import BeautifulSoup
import requests

class URLScraper:
    def scrape(self, url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract main content (customize based on site structure)
        paragraphs = soup.find_all('p')
        return ' '.join([p.get_text() for p in paragraphs])
```

## 📝 License

MIT License - Feel free to use this project for learning and development.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📞 Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Built with ❤️ for better reading comprehension**
