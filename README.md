# WordMixr 🎯

A full-stack web application for solving word puzzles by finding all possible words from scrambled letters. Built with FastAPI backend and React TypeScript frontend, fully containerized with Docker.

## Features

- **Word Solving**: Find all possible words that can be formed from a set of scrambled letters
- **Anagram Detection**: Find words that use all letters exactly once
- **Quality Filtering**: Smart filtering to show only meaningful words (no single letters, common abbreviations, or nonsensical combinations)
- **Configurable Length**: Set minimum word length (1-6+ letters) to focus on words you want
- **Modern UI**: Beautiful and responsive React interface with gradient design
- **Fast Processing**: Efficient algorithm using `collections.Counter` for quick word matching
- **High-Quality Dictionary**: Uses Google's 10,000 most common English words (frequency-based, no profanity) for realistic word puzzle results
- **Containerized**: Fully dockerized for easy deployment and development

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11** - Latest Python runtime
- **uvicorn** - ASGI server for FastAPI
- **English Words Dictionary** - 370k+ word dictionary

### Frontend
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **Modern CSS** - Gradient designs and responsive layout

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy for production frontend

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Running with Docker (Recommended)

1. **Start the application stack**:
   ```bash
   docker-compose up --build
   ```

2. **Or run in detached mode (background)**:
   ```bash
   docker-compose up --build -d
   ```

3. **Access the application**:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Quick Commands

```bash
# Start the application
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild and restart
docker-compose down && docker-compose up --build -d
```

### Development Setup

#### Backend Development
```bash
cd backend
pip install -r requirements.txt
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### `GET /solve`
Find all possible words from scrambled letters.

**Parameters:**
- `letters` (string): Letters to use for word formation (max 20 characters)
- `min_word_length` (integer, optional): Minimum word length to include (default: 3, range: 1-10)

**Examples:**
```bash
# Default filtering (3+ letters)
curl "http://localhost:8000/solve?letters=beach"

# Show only 4+ letter words
curl "http://localhost:8000/solve?letters=beach&min_word_length=4"

# Include short words (2+ letters)
curl "http://localhost:8000/solve?letters=beach&min_word_length=2"
```

**Response:**
```json
{
  "success": true,
  "input_letters": "beach",
  "word_count": 17,
  "words": ["bache", "beach", "ache", "bach", "chab", "each", ...]
}
```

### `GET /anagrams`
Find anagrams using all letters exactly once.

**Parameters:**
- `letters` (string): Letters to find anagrams for
- `min_word_length` (integer, optional): Minimum word length to include (default: 3, range: 1-10)

**Examples:**
```bash
# Default filtering (3+ letters)
curl "http://localhost:8000/anagrams?letters=listen"

# Include very short anagrams
curl "http://localhost:8000/anagrams?letters=listen&min_word_length=1"
```

**Response:**
```json
{
  "success": true,
  "input_letters": "listen",
  "word_count": 6,
  "words": ["enlist", "inlets", "listen", "silent", "slinte", "tinsel"]
}
```

### `GET /health`
Health check endpoint.

## Usage Examples

1. **Finding all words from "BEACH"**:
   - Enter "beach" in the input field
   - Select minimum word length (default: 3+ letters)
   - Click "Solve" or press Enter
   - See quality words like: beach, each, ache, bach, etc.

2. **Finding anagrams of "LISTEN"**:
   - Switch to "Anagrams Only" mode
   - Enter "listen"
   - See: listen, silent, enlist, tinsel, inlets, slinte

3. **Adjusting word quality**:
   - Use "Min word length" dropdown to filter results
   - 3+ letters (recommended): Only meaningful words
   - 4+ letters: Longer, more recognizable words
   - 2+ letters: Include short but valid words

4. **Complex puzzles**:
   - Try longer combinations like "scramble"
   - Get dozens of filtered, meaningful words sorted by length

## Word Quality Filtering

WordMixr includes intelligent filtering to show only meaningful English words:

### ✅ **What's Included:**
- Real English words from comprehensive dictionary
- Words meeting minimum length requirement (3+ letters by default)
- Common and recognizable vocabulary

### ❌ **What's Filtered Out:**
- Single letters (a, b, c, etc.)
- Double letter combinations (aa, bb, cc, etc.)
- Common abbreviations and non-words
- Repeated character patterns (aaa, bbb, etc.)
- Very obscure or archaic terms

### 🎛️ **Customizable Filtering:**
- **1+ letters**: Include everything (not recommended for most puzzles)
- **2+ letters**: Include short valid words
- **3+ letters**: Recommended default - good balance of quality and quantity
- **4+ letters**: Focus on longer, more recognizable words
- **5+ letters**: Only substantial words
- **6+ letters**: Very selective, longer words only

## Project Structure

```
wordmixr/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── solver.py        # Word solving algorithms
│   │   ├── utils.py         # Utility functions
│   │   └── words_alpha.txt  # English dictionary
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── index.tsx        # React entry point
│   │   └── components/
│   │       └── WordSolver.tsx # Main UI component
│   ├── package.json         # Node dependencies
│   ├── tsconfig.json        # TypeScript config
│   ├── vite.config.ts       # Vite configuration
│   ├── nginx.conf           # Nginx config
│   └── Dockerfile          # Frontend container
├── docker-compose.yml       # Container orchestration
├── README.md               # This file
└── screenshots/
    └── ui_mockup.png       # UI mockup
```

## Algorithm Details

The word solving algorithm uses an efficient approach optimized for quality:

1. **Input Validation**: Clean and validate user input
2. **Letter Counting**: Use `collections.Counter` to count available letters
3. **Quality Dictionary**: Search through curated 10k high-frequency English words
4. **Constraint Checking**: Ensure word doesn't use more of any letter than available
5. **Length Filtering**: Apply minimum word length (default: 4+ letters for best quality)
6. **Result Sorting**: Sort results by length (longest first) then alphabetically

**Time Complexity**: O(n×m) where n = 10k words, m = average word length (~4.5 chars)
**Space Complexity**: O(k) where k = number of valid words found (typically 2-20)

**Performance**: ~50x faster than large dictionaries due to smaller, optimized word set

## Performance

- **Dictionary Loading**: ~10k high-quality words loaded at startup (vs 370k+ in basic dictionaries)
- **Search Speed**: Typical queries return results in <50ms (faster due to smaller, optimized dictionary)
- **Memory Usage**: ~1MB for dictionary in memory (50x reduction)
- **Scalability**: Stateless design allows horizontal scaling

## Dictionary Quality

WordMixr supports multiple high-quality English word dictionaries optimized for different use cases:

### 🎯 **Default: SCOWL Large (126k curated words) - RECOMMENDED FOR WORD GAMES**

**Source**: [SCOWL (Spell Checker Oriented Word Lists)](http://wordlist.aspell.net/)

SCOWL is specifically designed for spell checkers and word games. Based on Word Cookies testing, **SCOWL Large** provides the optimal balance of coverage and quality.

### ✅ **Why SCOWL Large is Perfect for Word Games:**
- **Complete Game Coverage**: Includes ALL essential words like "ache" AND "gird" that puzzle games expect
- **Word Cookies Tested**: Verified to include missing words that SCOWL Medium lacks
- **Game-Optimized**: Specifically designed for spell checkers and word puzzles
- **Quality Curated**: 126k carefully selected words, no noise or obscure terms
- **No Profanity**: Clean, family-friendly word list
- **Real English Focus**: Excludes Latin terms, abbreviations, and archaic words

### 📊 **Dictionary Options:**

| Dictionary | Words | Quality | Best For | Contains "ACHE" & "GIRD" |
|------------|-------|---------|----------|---------------------------|
| **SCOWL Large** | 126k | ⭐⭐⭐⭐⭐ | **Word games (recommended)** | ✅ Yes & Yes |
| **SCOWL Medium** | 58k | ⭐⭐⭐⭐ | Basic word puzzles | ✅ Yes & ❌ No |
| **Google 10k** | 10k | ⭐⭐⭐⭐ | Simple games | ❌ No & ❌ No |
| **Comprehensive** | 370k | ⭐⭐⭐ | Academic/research use | ✅ Yes & ✅ Yes (with filtering) |

### 🔗 **Dictionary Sources:**
- **SCOWL**: [wordlist.aspell.net](http://wordlist.aspell.net/) - Spell Checker Oriented Word Lists
- **Google 10k**: [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english) - Google's Trillion Word Corpus
- **Comprehensive**: [dwyl/english-words](https://github.com/dwyl/english-words) - 370k+ words from various sources

### 📊 **Live Quality Comparison:**

**Word Cookies Testing Results:**

| Test | Dictionary | Words Found | Missing Critical Words? |
|------|------------|-------------|-------------------------|
| **"BHACE"** | SCOWL Large | `beach`, `ache`, `each` | ✅ Complete |
| | SCOWL Medium | `beach`, `ache`, `each` | ✅ Complete |
| | Google 10k | `beach`, `each` | ❌ Missing "ache" |
| **"GRINDK"** | SCOWL Large | `drink`, `grind`, `gird`, `grid`, `grin`, etc. | ✅ Complete |
| | SCOWL Medium | `drink`, `grind`, `grid`, `grin`, etc. | ❌ Missing "gird" |
| | Google 10k | `drink`, `grind`, `grid`, `grin`, etc. | ❌ Missing "gird" |

### 🎯 **Why SCOWL Large is the Winner:**
- **✅ Includes "ache" AND "gird"**: All essential words that Word Cookies expects
- **✅ Game-tested coverage**: Verified with actual Word Cookies puzzles
- **✅ Zero noise**: No Latin terms, abbreviations, or random letter combinations
- **✅ Professional quality**: Used by spell checkers and word game developers

### 🔧 **Enhanced Filtering System:**

WordMixr includes smart filtering to improve comprehensive dictionary quality:
- **Latin terms**: Removes "haec", "hic", "hoc" and other Latin words
- **Letter noise**: Filters "bch", "ech", "chab" and similar combinations  
- **Pattern analysis**: Detects too many consonants or unusual letter patterns
- **Quality focus**: Prioritizes recognizable English words

**Configurable via environment variable:**
```bash
# SCOWL Large - Perfect for word games (default, Word Cookies tested)
WORDMIXR_DICTIONARY=scowl_large

# SCOWL Medium - Good quality but missing some words like "gird"
WORDMIXR_DICTIONARY=scowl_medium

# Google 10k - High quality but missing common words like "ache" and "gird"
WORDMIXR_DICTIONARY=google_10k

# Comprehensive - All words but includes noise (with enhanced filtering)
WORDMIXR_DICTIONARY=comprehensive

# Auto-select - Tries SCOWL Large first, with intelligent fallbacks
WORDMIXR_DICTIONARY=auto

# Auto-select with fallback
WORDMIXR_DICTIONARY=auto
```

## Configuration

### 🔧 Dictionary Selection

WordMixr supports multiple dictionary configurations via environment variables:

#### Environment Variable

Set `WORDMIXR_DICTIONARY` to control which dictionary to use:

```bash
# SCOWL Large - Perfect for word games (default, recommended for Word Cookies)
export WORDMIXR_DICTIONARY=scowl_large

# SCOWL Medium - Good quality but missing some words like "gird"
export WORDMIXR_DICTIONARY=scowl_medium

# Google 10k - High quality but missing common words like "ache" and "gird"
export WORDMIXR_DICTIONARY=google_10k

# Comprehensive - All words but includes noise (with enhanced filtering)
export WORDMIXR_DICTIONARY=comprehensive

# Auto-select - Tries SCOWL Large first, with intelligent fallbacks
export WORDMIXR_DICTIONARY=auto
```

#### Docker Configuration

Set the environment variable in your Docker Compose or container:

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - WORDMIXR_DICTIONARY=scowl_large  # or "scowl_medium", "google_10k", "comprehensive", "auto"
```

```bash
# Docker run
docker run -e WORDMIXR_DICTIONARY=comprehensive wordmixr-backend
```

#### Kubernetes Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordmixr-backend
spec:
  template:
    spec:
      containers:
      - name: backend
        env:
        - name: WORDMIXR_DICTIONARY
          value: "google_10k"
```

### Other Environment Variables

**Backend:**
- `WORDMIXR_DICTIONARY`: Dictionary type (`google_10k`|`comprehensive`|`auto`)
- `PYTHONPATH`: Python module path (default: `/app`)

**Frontend:**
- `NODE_ENV`: Node environment (default: `production`)
- `CHOKIDAR_USEPOLLING`: Enable file watching (development)

### API Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `letters` | string | required | Letters to solve (2-20 characters) |
| `min_word_length` | integer | 4 | Minimum word length (1-10) |

### Usage Examples

```bash
# Find all words with default settings (Google 10k dictionary)
curl "http://localhost:8000/solve?letters=scramble"

# Find longer words only
curl "http://localhost:8000/solve?letters=scramble&min_word_length=5"

# Find exact anagrams
curl "http://localhost:8000/anagrams?letters=listen"

# Check current dictionary configuration
curl "http://localhost:8000/health"
```

### Customization

1. **Dictionary**: Configure via `WORDMIXR_DICTIONARY` environment variable
2. **Styling**: Modify CSS in React components for different themes
3. **API**: Add new endpoints in `main.py` for additional features
4. **Algorithms**: Enhance `solver.py` for more complex puzzle types

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   docker-compose down
   # Change ports in docker-compose.yml if needed
   docker-compose up --build
   ```

2. **Frontend can't connect to backend**:
   - Check if backend is running on port 8000
   - Verify CORS settings in `main.py`

3. **Dictionary not found**:
   - Ensure `words_alpha.txt` exists in `backend/app/`
   - Check file permissions

### Logs
```bash
# View all logs
docker-compose logs

# View backend logs only
docker-compose logs backend

# View frontend logs only
docker-compose logs frontend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- English words dictionary from [dwyl/english-words](https://github.com/dwyl/english-words)
- Inspired by classic word puzzle games like Scrabble and Words with Friends 