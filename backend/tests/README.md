# WordMixr Testing Suite

This directory contains comprehensive unit tests and functional tests for the WordMixr backend, including specific data quality tests to verify dictionary coverage.

## Test Organization

### 🧪 test_solver.py
**Core solver functionality and data quality tests**

#### TestDictionaryLoading
- Tests loading of all dictionary types (SCOWL Large, SCOWL Medium, Google 10k)
- Verifies dictionary sizes and basic structure
- **Critical word coverage tests**: Ensures "ache" and "gird" are present in SCOWL Large

#### TestDataQuality  
- **Word Cookies critical words**: Tests for words that were missing in earlier dictionary versions
- **Common 3-letter words**: Verifies coverage of frequent English words
- **Non-word filtering**: Ensures obvious non-words are excluded
- **Specific scenarios**: Tests the exact "bhace" and "grindk" cases that revealed missing words

#### TestSolverFunctions
- Unit tests for `find_valid_words()`, `get_anagrams()`, `is_valid_word()`
- Tests letter constraint logic (words can't use more letters than provided)
- Tests minimum length filtering
- Tests sorting behavior (shortest to longest, then alphabetical)

#### TestIntegration
- End-to-end tests using real dictionaries
- **Word Cookies BHACE scenario**: Ensures "ache", "beach", "each" are found
- **Word Cookies GRINDK scenario**: Ensures "gird", "grid", "grind", "drink" are found
- Dictionary size validation tests

### 🌐 test_api.py  
**API endpoint functional tests**

#### TestAPIEndpoints
- Health check endpoint validation
- Solve endpoint with various inputs
- Anagram endpoint functionality
- Input validation and error handling
- Response structure consistency
- **Critical word API tests**: Verifies missing words are now found via API

#### TestPerformance
- Large input handling
- Response time validation

#### TestCoverage
- **Missing words coverage**: Tests previously problematic words through API
- **Dictionary quality via API**: Ensures problematic words are filtered out

### ⚙️ test_config.py
**Configuration management tests**

#### TestConfiguration
- Dictionary type enum validation
- File path mappings
- Auto mode priority order
- Dictionary descriptions

#### TestEnvironmentConfiguration  
- Environment variable override testing
- Invalid value handling
- Default fallback behavior

## Running Tests

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_solver.py::TestDataQuality -v
pytest tests/test_api.py::TestAPIEndpoints -v
```

### Using the Test Runner
```bash
# Run comprehensive test suite with detailed reporting
python run_tests.py
```

The test runner provides:
- 🔬 Unit tests for core algorithms
- 📊 Data quality and dictionary coverage verification  
- 🌐 API integration testing
- ⚙️ Configuration validation
- 🎯 Critical word verification (ache, gird, etc.)

## Data Quality Focus

These tests specifically address the dictionary quality issues discovered during development:

### Missing Words Issues
- **"ache"**: Missing from Google 10k dictionary
- **"gird"**: Missing from Google 10k and SCOWL Medium dictionaries  
- **Word Cookies compatibility**: Ensures the app works with popular word puzzle games

### Test Scenarios
1. **BHACE letters** → Must find: ache, beach, each
2. **GRINDK letters** → Must find: gird, grid, grind, drink
3. **Common words** → Verify coverage of frequent English words
4. **Quality filtering** → Ensure Latin terms and nonsense words are excluded

### Coverage Verification
- SCOWL Large: 120k+ words with good game coverage
- SCOWL Medium: 58k+ words (missing some like "gird") 
- Google 10k: 10k words (limited coverage)
- Comprehensive: 370k+ words (needs quality filtering)

## Test Reports

Tests generate coverage reports in `htmlcov/` directory. Key metrics:
- Function coverage of solver algorithms
- Dictionary loading robustness  
- API endpoint reliability
- Critical word availability verification

## Continuous Integration

These tests are designed to:
1. Catch regressions in word finding algorithms
2. Verify dictionary changes don't break critical word coverage
3. Ensure API compatibility
4. Validate configuration management
5. Maintain data quality standards for word puzzle compatibility 