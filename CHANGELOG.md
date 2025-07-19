# Changelog

All notable changes to WordMixr will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive unit and functional test suite
- Data quality tests for critical word coverage
- Interactive word clicking functionality (mark words as found)
- Words display from shortest to longest alphabetically
- Support for multiple curated dictionaries (SCOWL Large, Medium, Google 10k)
- Environment variable configuration for dictionary selection
- Enhanced filtering for comprehensive dictionary quality
- Comprehensive developer documentation (DEVELOPER.md)

### Changed
- Default minimum word length changed from 4 to 3 letters
- Default dictionary changed to SCOWL Large for optimal word game coverage
- Word sorting changed to shortest-first then alphabetical
- Improved UI with word interaction and visual feedback

### Fixed
- Critical word coverage: "ache" and "gird" now included in default dictionary
- Word Cookies compatibility issues resolved
- Dictionary quality filtering improved

## [1.0.0] - 2024-01-XX (Initial Release)

### Added
- Full-stack word puzzle solver application
- FastAPI backend with word solving algorithms
- React TypeScript frontend with modern UI
- Docker containerization for easy deployment
- Multiple dictionary support (Google 10k, SCOWL, Comprehensive)
- Word solving and anagram finding functionality
- Responsive web interface with gradient design
- API documentation with OpenAPI/Swagger
- Health check endpoint for monitoring
- Input validation and error handling
- Configurable minimum word length filtering

### Security
- Input sanitization and validation
- CORS configuration for secure cross-origin requests
- No authentication required (stateless design)

---

## Version Guidelines

### Version Format: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes to API or core functionality
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Change Categories

- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes 