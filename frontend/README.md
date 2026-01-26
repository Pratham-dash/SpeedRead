# SpeedRead Frontend

Modern Spritz-style speed reading application built with pure vanilla JavaScript.

## Structure
```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # All styling and visual design
├── app.js              # Core application logic
├── package.json        # Project metadata
├── package-lock.json   # Dependency lock file
└── requirements.txt    # Python dependencies (none required)
```

## Running the Application

### Option 1: Direct Browser Open
Simply open `index.html` in any modern browser.

### Option 2: Local Server
```bash
cd frontend
python3 -m http.server 8000
```
Then visit: http://localhost:8000

## Features
- ⚡ Speed reading with adjustable WPM (250-1000)
- 🎯 ORP (Optimal Recognition Point) highlighting
- ⌨️ Keyboard shortcuts (Space: play/pause, R: restart)
- 📊 Real-time progress tracking
- 🎨 Clean, modern dark UI
- 📱 Responsive design

## Tech Stack
- HTML5
- CSS3 (Flexbox, CSS Variables)
- Vanilla JavaScript (ES6+)
- Zero external dependencies
