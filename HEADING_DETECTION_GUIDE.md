# Heading Detection Feature

## Overview
The SpeedRead app now intelligently detects headings and formatted text, making them display:
- **5x slower** than normal words (shown 5 times instead of once)
- With **extra pauses** before and after (2x longer than sentence pauses)
- **Visually distinct** with larger font, green ORP color, and bold weight

## What Gets Detected as Headings

### 1. **ALL CAPS TEXT**
Example: `CHAPTER ONE` or `INTRODUCTION`
- Must be at least 2 words OR 8+ characters
- Will display slower with green highlighting

### 2. **Section Headers with Colons**
Example: `Introduction:` or `Key Points:`
- Short text (1-5 words) ending with a colon
- Indicates a section header

### 3. **Short Standalone Lines**
Example: `Getting Started` or `How It Works`
- 1-5 words without sentence-ending punctuation
- At least one capitalized word
- Likely a title or heading

## Visual Styling

### Normal Words
- Font size: 56px
- ORP color: Red (#FF4444)
- Regular weight

### Heading Words
- Font size: 64px (larger)
- ORP color: Green (#4CAF50)
- Bold weight (700)
- Brighter text

## Speed Adjustments

| Element Type | Display Multiplier | Pauses |
|--------------|-------------------|---------|
| Normal word | 1x | None |
| Long word (7+ chars) | 3x | None |
| Word with comma | 3x | None |
| Sentence ending | 1x | 3 blank spaces after |
| **Heading/All-caps** | **5x** | **3 spaces before + 6 spaces after** |

## Testing Examples

### Test Text 1: Article Format
```
THE FUTURE OF AI

Introduction:
Artificial intelligence is rapidly transforming our world in unprecedented ways.

Key Benefits:
AI systems can process vast amounts of data quickly and accurately.

Conclusion
The technology continues to evolve at an amazing pace.
```

### Test Text 2: Tutorial Format
```
PYTHON BASICS

Getting Started
Python is an easy-to-learn programming language.

First Steps:
Install Python from the official website and verify your installation.
```

## How to Use

1. **Start the backend** (in Ubuntu terminal):
   ```bash
   cd ~/SpeedRead/backend
   source venv/bin/activate
   python app.py
   ```

2. **Start the frontend** (in another Ubuntu terminal):
   ```bash
   cd ~/SpeedRead/frontend
   python3 -m http.server 8000
   ```

3. **Open browser**: http://localhost:8000

4. **Paste text** with headings into the textarea

5. **Click "Load Text"** - the backend will detect headings

6. **Click Play** - watch headings display slower with green color

## API Configuration

The frontend sends `detect_headings: true` by default. To disable:
```javascript
// In app.js, change:
detect_headings: false  // Disable heading detection
```

## Adjusting Heading Speed

To change how slow headings display, edit the multiplier in:
`backend/services/word_preprocessor.py`

```python
# Line ~60-65
if is_heading or is_all_caps:
    multiplier = 5  # Change this number (1-10)
```

Higher number = slower display (e.g., 10 = 10 times slower)

## Troubleshooting

**Headings not detected?**
- Check that your text has clear heading patterns (all caps, colons, or short lines)
- Verify backend is connected (green dot next to "SpeedRead")

**Headings too slow?**
- Reduce the multiplier in `word_preprocessor.py`

**Want more heading patterns?**
- Edit `is_likely_heading()` in `backend/services/text_processor.py`
- Add custom detection logic for your specific text format
