# Contributing to WordMixr 🤝

Thank you for your interest in contributing to WordMixr! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Code Standards](#code-standards)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project is committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to adhere to our Code of Conduct:

- **Be respectful** and considerate in all interactions
- **Be collaborative** and help others learn and grow
- **Be inclusive** and welcome people of all backgrounds
- **Be constructive** when providing feedback
- **Be patient** with newcomers and different skill levels

## Getting Started

### Prerequisites
- Git
- Docker & Docker Compose
- Python 3.11+ (for backend development)
- Node.js 18+ (for frontend development)

### Quick Setup
```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/wordmixr.git
cd wordmixr

# 2. Create a feature branch
git checkout -b feature/amazing-feature

# 3. Set up development environment
docker-compose up --build
```

## Development Setup

### Full Development Environment

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Running Tests

#### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_solver.py::TestDataQuality -v
pytest tests/test_api.py::TestAPIEndpoints -v

# Run comprehensive test suite
python run_tests.py
```

#### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run tests with UI
npm run test:ui

# Generate coverage
npm run coverage
```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

#### 🐛 **Bug Fixes**
- Fix existing functionality that isn't working correctly
- Include test cases that reproduce the bug
- Update documentation if behavior changes

#### ✨ **New Features**
- Add new word solving capabilities
- Improve user interface and experience
- Add new dictionary sources or filtering options
- Enhance API functionality

#### 📚 **Documentation**
- Improve existing documentation
- Add examples and tutorials
- Fix typos and clarify instructions
- Translate documentation

#### 🧪 **Testing**
- Add test coverage for existing functionality
- Improve test quality and performance
- Add integration tests and data quality tests

#### 🔧 **Infrastructure**
- Improve build processes and CI/CD
- Optimize Docker configurations
- Enhance deployment procedures

### What NOT to Contribute

Please avoid these types of contributions:
- ❌ Large refactoring without prior discussion
- ❌ Changes that break existing API compatibility
- ❌ Adding dependencies without justification
- ❌ Style-only changes without functional improvements
- ❌ Duplicate functionality that already exists

## Pull Request Process

### Before Creating a Pull Request

1. **Check existing issues** to see if your contribution is already being worked on
2. **Create an issue** for new features or major changes to discuss the approach
3. **Fork the repository** and create a feature branch
4. **Make your changes** following our code standards
5. **Add tests** for any new functionality
6. **Update documentation** as needed

### Pull Request Checklist

- [ ] **Branch**: Created from latest `main` branch
- [ ] **Tests**: All tests pass (`pytest` and `npm test`)
- [ ] **Coverage**: New code has test coverage
- [ ] **Documentation**: Updated for any API or user-facing changes
- [ ] **Code Style**: Follows project code standards
- [ ] **Commits**: Clear, descriptive commit messages
- [ ] **Description**: PR description explains what and why
- [ ] **Breaking Changes**: Clearly marked if any

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tests added/updated for new functionality
- [ ] All existing tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings or errors introduced
```

### Review Process

1. **Automated Checks**: CI/CD pipeline must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Manual testing for user-facing changes
4. **Documentation**: Review of any documentation changes
5. **Approval**: Maintainer approval before merge

## Testing Requirements

### Test Coverage Requirements
- **New Features**: Must include comprehensive tests
- **Bug Fixes**: Must include regression tests
- **API Changes**: Must include integration tests
- **Data Quality**: Must verify dictionary coverage for word game compatibility

### Critical Test Scenarios
When contributing changes that affect word finding:

```python
# Must verify these critical word scenarios
test_cases = [
    ("bhace", ["ache", "beach", "each"]),     # Word Cookies BHACE
    ("grindk", ["gird", "grid", "grind"]),    # Word Cookies GRINDK
]
```

### Test Categories
- **Unit Tests**: Algorithm and function testing
- **Integration Tests**: API endpoint testing
- **Data Quality Tests**: Dictionary coverage verification
- **Performance Tests**: Response time validation
- **UI Tests**: Frontend component testing

## Code Standards

### Python (Backend)
```bash
# Code formatting
python -m black app/
python -m isort app/

# Linting
python -m flake8 app/
python -m mypy app/

# Standards
- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Maximum line length: 88 characters
```

### TypeScript (Frontend)
```bash
# Code formatting
npm run lint:fix
npm run format

# Standards
- Use TypeScript strict mode
- Follow ESLint configuration
- Use meaningful variable names
- Write JSDoc for complex functions
```

### General Guidelines
- **Clear naming**: Use descriptive variable and function names
- **Small functions**: Keep functions focused and small
- **Comments**: Explain complex logic, not obvious code
- **Error handling**: Include proper error handling and validation
- **Performance**: Consider performance implications of changes

## Reporting Issues

### Bug Reports

Use this template for bug reports:

```markdown
**Bug Description**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Enter '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. iOS]
- Browser: [e.g. chrome, safari]
- Version: [e.g. 22]

**Additional Context**
Any other context about the problem.
```

### Dictionary Quality Issues

For issues with missing words or dictionary quality:

```markdown
**Dictionary Issue**
Word(s) missing or incorrectly included.

**Missing Words**
List specific words that should be found but aren't:
- "example"
- "another"

**Test Case**
Letters used: "exampleletters"
Expected words: list expected words
Actual results: list what was found

**Game Context**
Which word game or puzzle this affects (e.g., Word Cookies, Scrabble).
```

## Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the requested feature.

**Problem Solved**
What problem does this feature solve?

**Proposed Solution**
Describe your proposed solution.

**Alternatives Considered**
Alternative solutions you've considered.

**Additional Context**
Screenshots, mockups, or examples.
```

### Feature Discussion Process

1. **Create Issue**: Use feature request template
2. **Community Discussion**: Allow for community input
3. **Design Review**: Technical feasibility assessment
4. **Implementation Plan**: Break down into actionable tasks
5. **Development**: Implementation with tests and documentation

## Recognition

### Contributors

All contributors are recognized in:
- **README.md**: Contributors section
- **CHANGELOG.md**: Version-specific contributions
- **GitHub**: Contributor graphs and statistics

### Types of Recognition
- **Code Contributors**: Direct code contributions
- **Documentation Contributors**: Documentation improvements
- **Testers**: Bug reports and testing assistance
- **Designers**: UI/UX improvements and feedback
- **Community**: Support and discussions

## Getting Help

### Where to Get Help
- **GitHub Issues**: Technical questions and discussions
- **GitHub Discussions**: General questions and community support
- **Documentation**: Check README.md and DEVELOPER.md first
- **Examples**: Look at existing code and tests for patterns

### Response Times
- **Bug Reports**: Within 48 hours
- **Feature Requests**: Within 1 week
- **Pull Requests**: Within 1 week
- **Questions**: Within 48 hours

## Development Tips

### Dictionary Development
- **Test Critical Words**: Always verify "ache", "gird", and other critical words
- **Performance**: Consider dictionary size impact on performance
- **Quality**: Ensure new dictionaries maintain word game compatibility

### API Development
- **Backward Compatibility**: Maintain API compatibility when possible
- **Documentation**: Update OpenAPI specifications
- **Testing**: Include comprehensive API tests

### Frontend Development
- **Responsive Design**: Ensure mobile compatibility
- **Accessibility**: Follow accessibility best practices
- **Performance**: Optimize for fast loading and interaction

Thank you for contributing to WordMixr! 🎉 