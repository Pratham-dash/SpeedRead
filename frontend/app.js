// SpeedRead - Spritz-style speed reader

// Config
const API_BASE_URL = window.API_BASE_URL;

// App state
const appState = {
    words: [],
    orp_data: [],  // Store ORP data from backend
    currentIndex: 0,
    isPlaying: false,
    speed: 300,
    intervalId: null,
    backendConnected: false
};

// DOM elements
const elements = {
    wordBefore: document.querySelector('.word-before'),
    wordORP: document.querySelector('.word-orp'),
    wordAfter: document.querySelector('.word-after'),
    playBtn: document.getElementById('playBtn'),
    pauseBtn: document.getElementById('pauseBtn'),
    restartBtn: document.getElementById('restartBtn'),
    speedSelector: document.getElementById('speedSelector'),
    currentWordEl: document.querySelector('.current-word'),
    totalWordsEl: document.querySelector('.total-words'),
    progressBar: document.querySelector('.progress-bar-fill'),
    textInput: document.getElementById('textInput'),
    loadTextBtn: document.getElementById('loadTextBtn'),
    statusIndicator: document.getElementById('statusIndicator')
};

async function checkBackendStatus() {
    console.log('Checking backend status...');
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000);
        
        console.log('Fetching from http://localhost:5000/health');
        const response = await fetch(`http://localhost:5000/health`, {
            method: 'GET',
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        console.log('Response status:', response.status, response.ok);
        
        if (response.ok) {
            appState.backendConnected = true;
            elements.statusIndicator.classList.add('connected');
            elements.statusIndicator.classList.remove('disconnected');
            console.log('Backend API is available');
            return true;
        }
    } catch (error) {
        console.error('Backend connection error:', error);
    }
    
    appState.backendConnected = false;
    elements.statusIndicator.classList.add('disconnected');
    elements.statusIndicator.classList.remove('connected');
    console.log('Using local processing');
    return false;
}

// Calculate ORP position for a word (research-backed positions)
function calculateORP(word) {
    const length = word.length;
    if (length === 1) return 0;
    if (length === 2) return 0;
    if (length === 3) return 1;
    if (length === 4) return 1;
    if (length === 5) return 1;
    if (length >= 6 && length <= 9) return 2;
    if (length >= 10 && length <= 13) return 3;
    return 4; // 14+ chars
}

function parseText(text) {
    if (!text || typeof text !== 'string') {
        return [];
    }
    return text
        .trim()
        .split(/\s+/)
        .filter(word => word.length > 0);
}

function splitWordByORP(word) {
    const orpIndex = calculateORP(word);
    
    return {
        before: word.substring(0, orpIndex),
        orp: word.charAt(orpIndex),
        after: word.substring(orpIndex + 1)
    };
}

function calculateDelay(wpm) {
    return Math.floor(60000 / wpm);
}

// Display word with ORP aligned to center line
function displayWord(word, isHeading = false) {
    if (!word) {
        clearDisplay();
        return;
    }
    
    const parts = splitWordByORP(word);
    elements.wordBefore.textContent = parts.before;
    elements.wordORP.textContent = parts.orp;
    elements.wordAfter.textContent = parts.after;
    
    // Apply heading styling
    const wordDisplay = document.querySelector('.word-display');
    if (isHeading) {
        wordDisplay.classList.add('heading-word');
    } else {
        wordDisplay.classList.remove('heading-word');
    }
    
    // Center ORP on vertical line using dynamic positioning
    requestAnimationFrame(() => {
        const orpElement = elements.wordORP;
        
        if (wordDisplay && orpElement) {
            const orpRect = orpElement.getBoundingClientRect();
            const displayRect = wordDisplay.getBoundingClientRect();
            const orpCenter = orpRect.left + (orpRect.width / 2);
            const displayCenter = displayRect.left + (displayRect.width / 2);
            const offset = displayCenter - orpCenter;
            wordDisplay.style.left = `calc(50% + ${offset}px)`;
        }
    });
}

function clearDisplay() {
    elements.wordBefore.textContent = '';
    elements.wordORP.textContent = '';
    elements.wordAfter.textContent = '';
    const wordDisplay = document.querySelector('.word-display');
    if (wordDisplay) {
        wordDisplay.style.left = '50%';
    }
}

function updateProgress() {
    const current = appState.currentIndex + 1;
    const total = appState.words.length;
    
    elements.currentWordEl.textContent = current;
    elements.totalWordsEl.textContent = total;
    const percentage = total > 0 ? (current / total) * 100 : 0;
    elements.progressBar.style.width = `${percentage}%`;
}

function updateButtons() {
    if (appState.isPlaying) {
        elements.playBtn.style.display = 'none';
        elements.pauseBtn.style.display = 'flex';
        elements.restartBtn.style.display = 'none';
    } else if (appState.currentIndex >= appState.words.length && appState.words.length > 0) {
        elements.playBtn.style.display = 'none';
        elements.pauseBtn.style.display = 'none';
        elements.restartBtn.style.display = 'flex';
    } else {
        elements.playBtn.style.display = 'flex';
        elements.pauseBtn.style.display = 'none';
        
        if (appState.currentIndex > 0) {
            elements.restartBtn.style.display = 'flex';
        } else {
            elements.restartBtn.style.display = 'none';
        }
    }
}

function showNextWord() {
    if (appState.currentIndex < appState.words.length) {
        const word = appState.words[appState.currentIndex];
        
        // Check if we have ORP data with heading info
        let isHeading = false;
        if (appState.orp_data && appState.orp_data[appState.currentIndex]) {
            isHeading = appState.orp_data[appState.currentIndex].is_heading || false;
        }
        
        displayWord(word, isHeading);
        appState.currentIndex++;
        updateProgress();
    } else {
        stop();
        updateButtons();
    }
}

function play() {
    if (appState.words.length === 0) {
        alert('Please load text first!');
        return;
    }
    
    if (appState.currentIndex >= appState.words.length) {
        restart();
        return;
    }
    
    appState.isPlaying = true;
    updateButtons();
    
    if (appState.currentIndex === 0) {
        showNextWord();
    }
    const delay = calculateDelay(appState.speed);
    appState.intervalId = setInterval(showNextWord, delay);
}

function pause() {
    appState.isPlaying = false;
    
    if (appState.intervalId) {
        clearInterval(appState.intervalId);
        appState.intervalId = null;
    }
    
    updateButtons();
}

function stop() {
    appState.isPlaying = false;
    
    if (appState.intervalId) {
        clearInterval(appState.intervalId);
        appState.intervalId = null;
    }
}

function restart() {
    stop();
    appState.currentIndex = 0;
    clearDisplay();
    updateProgress();
    updateButtons();
    setTimeout(() => play(), 100);
}

async function loadText() {
    const text = elements.textInput.value.trim();
    
    if (!text) {
        alert('Please enter some text to read!');
        return;
    }
    stop();
    elements.loadTextBtn.disabled = true;
    elements.loadTextBtn.textContent = 'Loading...';
    
    try {
        if (USE_BACKEND) {
            await loadTextFromBackend(text);
        } else {
            loadTextLocally(text);
        }
        
        if (appState.words.length === 0) {
            alert('No valid words found in the text!');
            return;
        }
        clearDisplay();
        updateProgress();
        updateButtons();
        elements.playBtn.disabled = false;
        
        console.log(`Loaded ${appState.words.length} words`);
        
    } catch (error) {
        console.error('Error loading text:', error);
        alert('Error connecting to backend. Using local processing as fallback.');
        loadTextLocally(text);
        clearDisplay();
        updateProgress();
        updateButtons();
        elements.playBtn.disabled = false;
    } finally {
        elements.loadTextBtn.disabled = false;
        elements.loadTextBtn.textContent = 'Load Text';
    }
}

async function loadTextFromBackend(text) {
    const response = await fetch(`${API_BASE_URL}/process-text`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: text,
            duplicate_long_words: true,
            add_sentence_pauses: true,
            detect_headings: true  // Enable heading detection
        })
    });
    
    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
        throw new Error('Backend processing failed');
    }
    
    appState.words = data.words;
    appState.orp_data = data.orp_data;  // Store ORP data with heading info
    appState.currentIndex = 0;
    appState.backendConnected = true;
    
    console.log('Backend API connected:', data.stats);
    console.log('Original count:', data.stats.original_count, 'Processed:', data.stats.processed_count);
}

function loadTextLocally(text) {
    appState.words = parseText(text);
    appState.currentIndex = 0;
    appState.backendConnected = false;
    console.log('Using local processing (backend not available)');
}

function changeSpeed() {
    const newSpeed = parseInt(elements.speedSelector.value);
    appState.speed = newSpeed;
    if (appState.isPlaying) {
        const wasPlaying = appState.isPlaying;
        pause();
        
        if (wasPlaying) {
            play();
        }
    }
    
    console.log(`Speed changed to ${newSpeed} WPM`);
}

function initializeEventListeners() {
    elements.playBtn.addEventListener('click', play);
    elements.pauseBtn.addEventListener('click', pause);
    elements.restartBtn.addEventListener('click', restart);
    elements.speedSelector.addEventListener('change', changeSpeed);
    elements.loadTextBtn.addEventListener('click', loadText);
    
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (appState.isPlaying) {
                pause();
            } else {
                play();
            }
        }
        if (e.code === 'KeyR' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            restart();
        }
    });
}

async function init() {
    console.log('SpeedRead application initialized');
    await checkBackendStatus();
    appState.speed = parseInt(elements.speedSelector.value);
    initializeEventListeners();
    updateProgress();
    updateButtons();
    
    // Sample text for demo with headings
    const sampleText = `SPEED READING GUIDE

Introduction:
Speed reading is a collection of techniques that aim to increase reading speed without significantly reducing comprehension or retention.

How It Works
The human brain can process information much faster than the average reading speed. By training your eyes and mind to work together more efficiently, you can dramatically improve your reading speed while maintaining understanding.

Key Benefits:
- Save time on reading tasks
- Process more information quickly
- Improve focus and concentration`;
    
    elements.textInput.value = sampleText;
    
    console.log('Ready to speed read!');
}

// Start app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
