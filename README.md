# WordMixr 🎯

[![CI](https://github.com/tekenstam/WordMixr/actions/workflows/ci.yml/badge.svg)](https://github.com/tekenstam/WordMixr/actions/workflows/ci.yml)
[![Release](https://github.com/tekenstam/WordMixr/actions/workflows/release.yml/badge.svg)](https://github.com/tekenstam/WordMixr/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![PWA](https://img.shields.io/badge/PWA-Enabled-purple.svg)](https://web.dev/progressive-web-apps/)
[![Dependabot](https://img.shields.io/badge/Dependabot-Enabled-brightgreen.svg)](https://github.com/dependabot)

A full-stack web application for solving word puzzles by finding all possible words from scrambled letters. Features a beautiful custom brand identity with warm colors and friendly design, optimized for popular word games like Word Cookies.

## Features

- **Word Solving**: Find all possible words from scrambled letters
- **Anagram Detection**: Find words that use all letters exactly once
- **Interactive UI**: Click words to mark them as found, with visual feedback
- **Quality Dictionaries**: Multiple curated word lists optimized for word games
- **Smart Filtering**: Intelligent filtering to show only meaningful English words
- **Configurable Length**: Set minimum word length to focus on desired words
- **Fast & Modern**: Built with FastAPI + React TypeScript, fully containerized
- **Beautiful Design**: Custom brand identity with warm colors and friendly typography

## Quick Start

### Prerequisites
- Docker and Docker Compose

### 1. Download and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/wordmixr.git
cd wordmixr

# Start the application
docker compose up --build
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 3. Try It Out

1. **Enter letters** (e.g., "beach", "scramble", "listen")
2. **Set minimum word length** (3+ letters recommended)
3. **Click "Solve Words"** to find all possible words
4. **Click words** to mark them as found (they'll move to bottom and grey out)
5. **Try "Find Anagrams"** for exact letter matches

## 🤖 Automated Dependency Management

WordMixr uses **Dependabot** to automatically keep dependencies up-to-date:

- **📦 Frontend**: npm packages (React, TypeScript, Vite)
- **🐍 Backend**: Python packages (FastAPI, Pydantic)
- **🐳 Docker**: Base images and Docker actions
- **⚡ GitHub Actions**: Workflow dependencies

Dependabot runs weekly and creates PRs for security updates and version bumps. See [`docs/DEPENDABOT.md`](docs/DEPENDABOT.md) for detailed configuration.

## Common Commands

```bash
# Start application (detached)
docker compose up --build -d

# View logs
docker compose logs -f

# Stop application
docker compose down

# Restart with fresh build
docker compose down && docker compose up --build -d
```

## Example Usage

**Find words from "BEACH":**
- Results: `beach`, `each`, `ache`, `bach`, `cab`, `ace`
- Interactive: Click words to mark as found

**Find anagrams of "LISTEN":**
- Results: `listen`, `silent`, `enlist`, `tinsel`, `inlets`

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: React 18 + TypeScript + Vite
- **Infrastructure**: Docker + Docker Compose
- **Dictionaries**: SCOWL Large (126k curated words, optimized for word games)

## Word Quality

WordMixr uses **SCOWL Large dictionary** (126k curated words) by default, specifically optimized for word puzzle games:

✅ **Includes critical words** like "ache" and "gird" that other dictionaries miss  
✅ **No profanity** - family-friendly word list  
✅ **No noise** - excludes Latin terms, abbreviations, and nonsensical combinations  
✅ **Game-tested** - verified with Word Cookies and similar puzzle games  

## Need More?

For technical details, development setup, testing, API documentation, and deployment:

📖 **See [DEVELOPER.md](DEVELOPER.md)** for comprehensive documentation

## Troubleshooting

**Port already in use:**
```bash
docker compose down
# Edit ports in docker-compose.yml if needed
docker compose up --build
```

**Can't connect to backend:**
- Ensure backend is running: `curl http://localhost:8000/health`
- Check Docker logs: `docker compose logs backend`

**Dictionary issues:**
- Verify dictionary files exist in `backend/app/`
- Check configuration: `curl http://localhost:8000/health`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

See [DEVELOPER.md](DEVELOPER.md) for detailed development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Dictionaries**: [SCOWL](http://wordlist.aspell.net/), [Google 10k](https://github.com/first20hours/google-10000-english), [English Words](https://github.com/dwyl/english-words)
- **Inspiration**: Word Cookies, Scrabble, Words with Friends 