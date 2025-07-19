# WordMixr Developer Documentation 🔧

Comprehensive technical documentation for WordMixr development, testing, building, and deployment.

## Table of Contents

- [Development Setup](#development-setup)
- [Architecture & Design](#architecture--design)
- [Testing](#testing)
- [Building & Deployment](#building--deployment)
- [API Reference](#api-reference)
- [Algorithm Details](#algorithm-details)
- [Dictionary Management](#dictionary-management)
- [Configuration](#configuration)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Local Development

#### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run in development mode
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Alternative: Run with Python
python main.py
```

**Backend will be available at**: http://localhost:8000
**API Documentation**: http://localhost:8000/docs

#### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Frontend will be available at**: http://localhost:5173 (Vite dev server)

#### Full Stack Development
```bash
# Terminal 1: Backend
cd backend && pip install -r requirements.txt
cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend  
cd frontend && npm install && npm run dev
```

### Development Tools

#### Code Quality
```bash
# Backend linting
cd backend
python -m flake8 app/
python -m black app/
python -m mypy app/

# Frontend linting
cd frontend
npm run lint
npm run lint:fix
```

#### Git Hooks
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Architecture & Design

### Tech Stack

#### Backend
- **FastAPI** - Modern, fast Python web framework
- **Python 3.11** - Latest Python runtime with performance improvements
- **uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation and serialization
- **Collections.Counter** - Efficient letter counting algorithm

#### Frontend
- **React 18** - Modern React with concurrent features
- **TypeScript** - Type-safe JavaScript development
- **Vite** - Fast build tool and HMR dev server
- **Modern CSS** - Custom CSS with gradients and responsive design

#### Infrastructure
- **Docker** - Containerization for consistent environments
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Production-grade reverse proxy and static file serving

### Project Structure

```
wordmixr/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── solver.py            # Core word solving algorithms
│   │   ├── config.py            # Configuration management
│   │   ├── utils.py             # Utility functions
│   │   ├── words_alpha.txt      # Comprehensive English dictionary
│   │   ├── google-10000-english.txt  # Google 10k frequency list
│   │   ├── scowl-medium.txt     # SCOWL medium curated dictionary
│   │   └── scowl-large.txt      # SCOWL large curated dictionary
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_solver.py       # Unit tests for solver algorithms
│   │   ├── test_api.py          # API functional tests
│   │   ├── test_config.py       # Configuration tests
│   │   └── README.md            # Testing documentation
│   ├── requirements.txt         # Python dependencies
│   ├── pytest.ini              # pytest configuration
│   ├── run_tests.py             # Test runner script
│   └── Dockerfile              # Backend container
├── frontend/
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── src/
│   │   ├── App.tsx              # Main React application
│   │   ├── index.tsx            # React entry point
│   │   ├── setupTests.ts        # Test setup configuration
│   │   └── components/
│   │       ├── WordSolver.tsx   # Main UI component
│   │       └── __tests__/
│   │           └── WordSolver.test.tsx  # Component tests
│   ├── package.json             # Node dependencies and scripts
│   ├── tsconfig.json            # TypeScript configuration
│   ├── vite.config.ts           # Vite build configuration
│   ├── vitest.config.ts         # Vitest test configuration
│   ├── nginx.conf               # Nginx configuration
│   └── Dockerfile              # Frontend container
├── docker-compose.yml           # Container orchestration
├── PROMPT.md                    # Original project requirements
├── WordMixr_Prompt.md          # Detailed project specification
└── screenshots/
    └── ui_mockup.png           # UI design mockup
```

### API Design

The backend follows REST principles with these design decisions:

- **Stateless**: No server-side sessions, each request is independent
- **JSON**: All responses in JSON format with consistent structure
- **Error Handling**: Structured error responses with HTTP status codes
- **Validation**: Pydantic models for request/response validation
- **Documentation**: Auto-generated OpenAPI/Swagger docs

#### Response Structure
```json
{
  "success": true,
  "input_letters": "beach",
  "word_count": 17,
  "words": ["ache", "bach", "beach", "cab", "each"],
  "errors": [],
  "processing_time_ms": 12.5
}
```

#### Error Response Structure
```json
{
  "success": false,
  "error": "Invalid input",
  "errors": ["Letters parameter is required"],
  "input_letters": "",
  "word_count": 0,
  "words": []
}
```

## Testing

### Backend Testing

#### Test Organization
- **Unit Tests**: Core algorithms and functions
- **Integration Tests**: API endpoints and real dictionary usage
- **Data Quality Tests**: Dictionary coverage and word validation
- **Performance Tests**: Response time and load handling

#### Running Tests
```bash
cd backend

# Install test dependencies
pip install -r requirements.txt

# Run all tests with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_solver.py::TestDataQuality -v
pytest tests/test_api.py::TestAPIEndpoints -v
pytest tests/test_config.py -v

# Run comprehensive test suite
python run_tests.py
```

#### Test Categories

**🔬 Unit Tests (test_solver.py)**
- Core algorithm testing (find_valid_words, get_anagrams)
- Letter constraint validation
- Sorting and filtering logic
- Dictionary loading mechanisms

**📊 Data Quality Tests**
- Critical word coverage (ache, gird, beach, etc.)
- Common word verification
- Non-word filtering validation
- Dictionary size expectations

**🌐 API Tests (test_api.py)**
- Endpoint functionality
- Input validation
- Error handling
- Response structure consistency

**⚙️ Configuration Tests (test_config.py)**
- Environment variable handling
- Dictionary selection logic
- File path resolution

#### Critical Word Testing

The tests specifically verify words that were missing in earlier versions:

```bash
# Test Word Cookies scenarios
pytest tests/test_solver.py::TestIntegration::test_word_cookies_bhace_scenario -v
pytest tests/test_solver.py::TestIntegration::test_word_cookies_grindk_scenario -v

# Test data quality
pytest tests/test_solver.py::TestDataQuality::test_word_cookies_critical_words -v
```

**Verified Critical Words:**
- ✅ "ache" (missing in Google 10k)
- ✅ "gird" (missing in Google 10k and SCOWL Medium)
- ✅ "beach", "each", "drink", "grind", "grid", "grin"

### Frontend Testing

#### Setup
```bash
cd frontend

# Install test dependencies
npm install

# Run tests
npm test

# Run tests with UI
npm run test:ui

# Generate coverage report
npm run coverage
```

#### Test Structure
```typescript
// Component testing example
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import WordSolver from '../WordSolver'

describe('WordSolver Component', () => {
  it('handles word solving functionality', async () => {
    // Test implementation
  })
})
```

### Continuous Integration

#### GitHub Actions (Example)
```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          pytest --cov=app --cov-report=xml
          
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: |
          cd frontend
          npm install
          npm run test
          npm run build
```

## Building & Deployment

### Docker Build

#### Development Build
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build with no cache
docker-compose build --no-cache
```

#### Production Build
```bash
# Production optimization
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Multi-stage build for optimization
docker build -t wordmixr-backend:latest -f backend/Dockerfile backend/
docker build -t wordmixr-frontend:latest -f frontend/Dockerfile frontend/
```

### Release Process

#### Version Management
```bash
# Update version in package.json and setup.py
# Tag release
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# Build release images
docker build -t wordmixr-backend:v1.2.0 backend/
docker build -t wordmixr-frontend:v1.2.0 frontend/

# Push to registry
docker push wordmixr-backend:v1.2.0
docker push wordmixr-frontend:v1.2.0
```

#### Deployment Strategies

**1. Docker Compose (Simple)**
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Update deployment
docker-compose pull
docker-compose up -d --no-deps backend frontend
```

**2. Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordmixr-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wordmixr-backend
  template:
    metadata:
      labels:
        app: wordmixr-backend
    spec:
      containers:
      - name: backend
        image: wordmixr-backend:v1.2.0
        ports:
        - containerPort: 8000
        env:
        - name: WORDMIXR_DICTIONARY
          value: "scowl_large"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**3. Cloud Deployment (AWS/GCP/Azure)**
```bash
# Example: AWS ECS deployment
aws ecs update-service --cluster wordmixr --service wordmixr-backend --force-new-deployment

# Example: Google Cloud Run
gcloud run deploy wordmixr-backend --image gcr.io/project/wordmixr-backend:v1.2.0
```

### Environment Configuration

#### Production Environment Variables
```bash
# Backend
WORDMIXR_DICTIONARY=scowl_large
PYTHONPATH=/app
WORKERS=4
LOG_LEVEL=info

# Frontend
NODE_ENV=production
VITE_API_URL=https://api.wordmixr.com

# Infrastructure
POSTGRES_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://redis:6379/0
```

## API Reference

### Authentication
Currently no authentication required. Consider adding API keys for production:

```python
# Future authentication example
@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        api_key = request.headers.get("X-API-Key")
        if not validate_api_key(api_key):
            return JSONResponse(status_code=401, content={"error": "Invalid API key"})
    return await call_next(request)
```

### Endpoints

#### `GET /solve`
Find all possible words from scrambled letters.

**Parameters:**
- `letters` (string, required): Letters to use (2-20 characters)
- `min_word_length` (integer, optional): Minimum word length (1-10, default: 3)

**Request Examples:**
```bash
# Basic usage
curl "http://localhost:8000/solve?letters=beach"

# With minimum length
curl "http://localhost:8000/solve?letters=beach&min_word_length=4"

# Complex puzzle
curl "http://localhost:8000/solve?letters=scramble&min_word_length=3"
```

**Response:**
```json
{
  "success": true,
  "input_letters": "beach",
  "word_count": 17,
  "words": ["ace", "ache", "bach", "beach", "cab", "each"],
  "processing_time_ms": 12.5,
  "dictionary_info": {
    "type": "scowl_large",
    "size": 126000,
    "description": "SCOWL Large dictionary - optimal for word games"
  }
}
```

#### `GET /anagrams`
Find exact anagrams using all letters once.

**Parameters:**
- `letters` (string, required): Letters to find anagrams for
- `min_word_length` (integer, optional): Minimum word length (default: 3)

**Request Examples:**
```bash
curl "http://localhost:8000/anagrams?letters=listen"
curl "http://localhost:8000/anagrams?letters=restful&min_word_length=4"
```

**Response:**
```json
{
  "success": true,
  "input_letters": "listen",
  "word_count": 6,
  "words": ["enlist", "inlets", "listen", "silent", "slinte", "tinsel"],
  "processing_time_ms": 8.2
}
```

#### `GET /health`
System health and configuration information.

**Response:**
```json
{
  "status": "healthy",
  "dictionary_loaded": true,
  "dictionary_size": 126000,
  "dictionary_info": {
    "type": "scowl_large",
    "filepath": "/app/scowl-large.txt",
    "description": "SCOWL Large dictionary - optimal for word games"
  },
  "configuration": {
    "dictionary_type": "scowl_large",
    "environment_var": "WORDMIXR_DICTIONARY",
    "available_types": ["google_10k", "scowl_medium", "scowl_large", "comprehensive", "auto"]
  }
}
```

### Error Handling

#### Error Response Format
```json
{
  "success": false,
  "error": "Validation error",
  "errors": ["Letters must be between 2 and 20 characters"],
  "input_letters": "",
  "word_count": 0,
  "words": []
}
```

#### HTTP Status Codes
- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Algorithm Details

### Word Solving Algorithm

#### Core Logic
```python
def find_valid_words(letters: str, dictionary: set, min_length: int = 3) -> list:
    """
    Find all valid words using optimized letter counting.
    
    Time Complexity: O(n×m) where n=dictionary size, m=average word length
    Space Complexity: O(k) where k=number of valid words found
    """
    letter_count = Counter(letters.lower())
    valid_words = []
    
    for word in dictionary:
        if len(word) >= min_length and is_valid_word(word):
            word_count = Counter(word)
            if all(word_count[char] <= letter_count[char] for char in word_count):
                valid_words.append(word)
    
    return sorted(valid_words, key=lambda x: (len(x), x))
```

#### Optimization Strategies

**1. Dictionary Pre-filtering**
- Remove words with repeated patterns (aaa, bbb)
- Filter out non-English words and abbreviations
- Use curated word lists (SCOWL) for better quality

**2. Counter-based Matching**
- Use `collections.Counter` for O(1) letter frequency checking
- Early termination when word requirements exceed available letters

**3. Memory Optimization**
- Load dictionary once at startup
- Use sets for O(1) word lookup
- Minimize string operations

**4. Response Sorting**
- Sort by length first (shorter words first for UI)
- Then alphabetically for predictable ordering
- Consider caching common results

### Performance Benchmarks

#### Dictionary Comparison
| Dictionary | Size | Load Time | Search Time | Memory |
|------------|------|-----------|-------------|---------|
| Google 10k | 10k | ~20ms | ~10ms | ~0.5MB |
| SCOWL Medium | 58k | ~80ms | ~25ms | ~2MB |
| SCOWL Large | 126k | ~150ms | ~45ms | ~4MB |
| Comprehensive | 370k | ~500ms | ~120ms | ~15MB |

#### Typical Performance
- **Cold start**: 150ms (dictionary loading)
- **Warm queries**: 10-50ms (depending on dictionary size)
- **Memory usage**: 2-15MB (depending on dictionary)
- **Concurrent users**: 100+ (stateless design)

## Dictionary Management

### Available Dictionaries

#### 🎯 SCOWL Large (Recommended)
- **Size**: 126k curated words
- **Source**: [SCOWL (Spell Checker Oriented Word Lists)](http://wordlist.aspell.net/)
- **Best for**: Word games, puzzles, general use
- **Quality**: ⭐⭐⭐⭐⭐
- **Coverage**: Includes all critical words like "ache" and "gird"

#### 📊 SCOWL Medium  
- **Size**: 58k curated words
- **Best for**: Basic word puzzles
- **Quality**: ⭐⭐⭐⭐
- **Limitations**: Missing some words like "gird"

#### 🔤 Google 10k
- **Size**: 10k high-frequency words
- **Source**: [Google Trillion Word Corpus](https://github.com/first20hours/google-10000-english)
- **Best for**: Simple games, fast performance
- **Quality**: ⭐⭐⭐⭐
- **Limitations**: Missing common words like "ache" and "gird"

#### 📚 Comprehensive
- **Size**: 370k+ words
- **Source**: [DWYL English Words](https://github.com/dwyl/english-words)
- **Best for**: Academic use, maximum coverage
- **Quality**: ⭐⭐⭐ (includes noise)
- **Note**: Requires enhanced filtering

### Dictionary Testing

#### Critical Word Coverage Tests
```python
# Test specific game scenarios
test_cases = [
    {
        "letters": "bhace",
        "critical_words": ["ache", "beach", "each"],
        "description": "Word Cookies BHACE scenario"
    },
    {
        "letters": "grindk", 
        "critical_words": ["gird", "grid", "grind", "drink"],
        "description": "Word Cookies GRINDK scenario"
    }
]
```

#### Quality Metrics
- **Coverage**: Percentage of common words included
- **Noise ratio**: Percentage of non-words or obscure terms
- **Game compatibility**: Success rate with popular word games
- **Performance**: Search speed and memory usage

### Adding New Dictionaries

#### Process
1. **Source**: Find reputable word list source
2. **Format**: Convert to lowercase, one word per line
3. **Quality**: Apply filtering for non-English and duplicates
4. **Test**: Verify coverage with critical word tests
5. **Configure**: Add to `config.py` dictionary mappings
6. **Document**: Update documentation and recommendations

#### Example Integration
```python
# config.py
DICTIONARY_FILES = {
    DictionaryType.CUSTOM: [
        "custom-dictionary.txt",
        "/app/custom-dictionary.txt",
        "app/custom-dictionary.txt"
    ]
}

def _get_dictionary_description(dict_type: DictionaryType) -> str:
    descriptions = {
        DictionaryType.CUSTOM: "Custom curated word list for specific domain"
    }
    return descriptions.get(dict_type, "Unknown dictionary type")
```

## Configuration

### Environment Variables

#### Backend Configuration
```bash
# Dictionary selection (primary configuration)
WORDMIXR_DICTIONARY=scowl_large  # google_10k|scowl_medium|scowl_large|comprehensive|auto

# Server configuration
HOST=0.0.0.0
PORT=8000
WORKERS=1
LOG_LEVEL=info

# Development
RELOAD=true
DEBUG=false

# Future: Database configuration
DATABASE_URL=postgresql://user:pass@host:5432/wordmixr
REDIS_URL=redis://redis:6379/0
```

#### Frontend Configuration
```bash
# Build configuration
NODE_ENV=production
VITE_API_URL=http://localhost:8000

# Development
CHOKIDAR_USEPOLLING=true
```

### Docker Compose Configuration

#### Development
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - WORDMIXR_DICTIONARY=scowl_large
      - RELOAD=true
      - LOG_LEVEL=debug
  frontend:
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
```

#### Production
```yaml
# docker-compose.prod.yml
services:
  backend:
    environment:
      - WORDMIXR_DICTIONARY=scowl_large
      - WORKERS=4
      - LOG_LEVEL=info
  frontend:
    environment:
      - NODE_ENV=production
```

### Runtime Configuration

#### Health Check Endpoint
```bash
# Check current configuration
curl http://localhost:8000/health | jq .configuration

# Example response
{
  "dictionary_type": "scowl_large",
  "environment_var": "WORDMIXR_DICTIONARY",
  "available_types": ["google_10k", "scowl_medium", "scowl_large", "comprehensive", "auto"]
}
```

## Performance

### Optimization Strategies

#### Backend Optimizations
1. **Dictionary Caching**: Load once at startup
2. **Algorithm Efficiency**: Counter-based letter matching
3. **Memory Management**: Use sets for O(1) lookups
4. **Response Compression**: Gzip compression for large responses

#### Frontend Optimizations
1. **Code Splitting**: Lazy load components
2. **Debouncing**: Delay API calls during typing
3. **Caching**: Cache recent results in localStorage
4. **Virtualization**: For large result lists

#### Infrastructure Optimizations
1. **Container Optimization**: Multi-stage Docker builds
2. **Static Assets**: CDN for frontend assets
3. **Load Balancing**: Multiple backend instances
4. **Caching Layer**: Redis for API response caching

### Monitoring & Profiling

#### Backend Profiling
```python
# Add performance monitoring
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {(end - start) * 1000:.2f}ms")
        return result
    return wrapper

@timing_decorator
def find_valid_words(letters, dictionary, min_length=3):
    # Implementation
```

#### Performance Metrics
```bash
# Monitor API performance
curl -w "@curl-format.txt" "http://localhost:8000/solve?letters=complicated"

# Example curl-format.txt
time_namelookup:  %{time_namelookup}s
time_connect:     %{time_connect}s
time_appconnect:  %{time_appconnect}s
time_pretransfer: %{time_pretransfer}s
time_redirect:    %{time_redirect}s
time_starttransfer: %{time_starttransfer}s
time_total:       %{time_total}s
```

### Load Testing
```bash
# Install load testing tools
pip install locust

# Run load tests
locust -f locustfile.py --host http://localhost:8000
```

```python
# locustfile.py
from locust import HttpUser, task, between

class WordMixrUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def solve_words(self):
        self.client.get("/solve?letters=scramble&min_word_length=3")
    
    @task(1)
    def find_anagrams(self):
        self.client.get("/anagrams?letters=listen")
    
    @task(1)
    def health_check(self):
        self.client.get("/health")
```

## Troubleshooting

### Common Issues

#### Backend Issues

**1. Dictionary Not Loading**
```bash
# Check if dictionary files exist
ls -la backend/app/*.txt

# Verify file permissions
chmod 644 backend/app/*.txt

# Check dictionary configuration
curl http://localhost:8000/health | jq .dictionary_info
```

**2. Import Errors**
```bash
# Check Python path
export PYTHONPATH=/app:$PYTHONPATH

# Verify dependencies
cd backend && pip check
```

**3. Performance Issues**
```bash
# Check dictionary size and type
curl http://localhost:8000/health | jq .dictionary_size

# Switch to smaller dictionary
export WORDMIXR_DICTIONARY=google_10k
```

#### Frontend Issues

**1. API Connection Issues**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify CORS configuration in main.py
# Check network connectivity
```

**2. Build Issues**
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors
npm run type-check
```

#### Docker Issues

**1. Port Conflicts**
```bash
# Check what's using ports
lsof -i :3000
lsof -i :8000

# Change ports in docker-compose.yml
```

**2. Container Build Issues**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Debugging

#### Backend Debugging
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debugger
import pdb; pdb.set_trace()

# Profile performance
import cProfile
cProfile.run('find_valid_words("scramble", dictionary)')
```

#### Frontend Debugging
```typescript
// Add console debugging
console.log('API Response:', response)

// Use React DevTools
// Browser Developer Tools Network tab
```

### Log Analysis

#### Backend Logs
```bash
# View backend logs
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# Filter by level
docker-compose logs backend | grep ERROR
```

#### Frontend Logs
```bash
# View frontend build logs
docker-compose logs frontend

# Check for JavaScript errors in browser console
```

### Health Monitoring

#### Endpoint Monitoring
```bash
# Health check script
#!/bin/bash
while true; do
  status=$(curl -s http://localhost:8000/health | jq -r .status)
  if [ "$status" != "healthy" ]; then
    echo "Service unhealthy: $status"
    # Alert or restart service
  fi
  sleep 30
done
```

#### Resource Monitoring
```bash
# Monitor container resources
docker stats

# Monitor disk usage
du -sh backend/app/*.txt

# Monitor memory usage
ps aux | grep python
```

## Contributing

### Development Workflow

#### Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/wordmixr.git
cd wordmixr

# Create development branch
git checkout -b feature/new-feature

# Setup development environment
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

#### Code Standards

**Python (Backend)**
```bash
# Follow PEP 8
python -m black app/
python -m flake8 app/
python -m mypy app/

# Test coverage
pytest --cov=app --cov-report=html
```

**TypeScript (Frontend)**
```bash
# ESLint and Prettier
npm run lint
npm run lint:fix
npm run format

# Type checking
npm run type-check
```

#### Testing Requirements
- All new features must include tests
- Maintain >90% test coverage
- Include integration tests for API changes
- Add data quality tests for dictionary changes

#### Pull Request Process
1. **Create feature branch** from main
2. **Implement changes** with tests
3. **Run full test suite** locally
4. **Update documentation** if needed
5. **Submit pull request** with clear description
6. **Address review feedback**
7. **Squash and merge** after approval

#### Documentation Standards
- Update API documentation for endpoint changes
- Add code comments for complex algorithms
- Update README/DEVELOPER.md for user-facing changes
- Include examples for new features

### Release Process

#### Versioning
Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

#### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] Docker images built and tested
- [ ] Performance benchmarks verified
- [ ] Security scan completed

## License & Acknowledgments

### License
This project is open source and available under the [MIT License](LICENSE).

### Acknowledgments

**Dictionaries:**
- **SCOWL**: [wordlist.aspell.net](http://wordlist.aspell.net/) - Spell Checker Oriented Word Lists
- **Google 10k**: [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english)
- **English Words**: [dwyl/english-words](https://github.com/dwyl/english-words)

**Inspiration:**
- Classic word puzzle games (Scrabble, Words with Friends, Word Cookies)
- Modern web development best practices
- Open source community contributions

**Tools & Frameworks:**
- FastAPI and React teams for excellent frameworks
- Docker for containerization technology
- Testing frameworks (pytest, Vitest) for quality assurance 