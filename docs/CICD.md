# CI/CD Pipeline Documentation 🚀

This document describes WordMixr's comprehensive CI/CD pipeline built with GitHub Actions.

## Overview

WordMixr uses a two-stage pipeline approach:
1. **Continuous Integration (CI)** - Runs on every PR and push to main
2. **Continuous Deployment (CD)** - Triggers on version tags for automated releases

## Continuous Integration (.github/workflows/ci.yml)

### Trigger Events
- Pull requests to `main` or `master` branches
- Direct pushes to `main` or `master` branches

### Pipeline Jobs

#### 1. Backend Tests & Quality (backend-tests)
**Purpose**: Ensure backend code quality and functionality
**Steps**:
- ✅ Code formatting check (Black)
- ✅ Import sorting check (isort)  
- ✅ Linting (flake8)
- ✅ Type checking (mypy)
- ✅ Security scanning (bandit)
- ✅ Unit tests with coverage
- ✅ **Data quality tests** (critical word coverage)
- ✅ API integration tests

**Critical Features**:
- Tests specifically verify "ache" and "gird" word coverage
- Validates Word Cookies compatibility scenarios
- Ensures dictionary quality standards

#### 2. Frontend Tests & Quality (frontend-tests)
**Purpose**: Ensure frontend code quality and functionality
**Steps**:
- ✅ TypeScript type checking
- ✅ Linting (ESLint)
- ✅ Code formatting check (Prettier)
- ✅ Unit tests with coverage
- ✅ Build verification

#### 3. Docker Build Verification (docker-build)
**Purpose**: Verify containerization works correctly
**Steps**:
- ✅ Build backend Docker image
- ✅ Build frontend Docker image
- ✅ Use build caching for performance

#### 4. End-to-End Tests (e2e-tests)
**Purpose**: Test the complete application stack
**Steps**:
- ✅ Start full application stack
- ✅ Test critical word scenarios
- ✅ Test API error handling
- ✅ Verify dictionary quality
- ✅ **WordMixr-specific testing**:
  - BHACE scenario (ache, beach, each)
  - GRINDK scenario (gird, grid, grind, drink)
  - Anagram functionality

#### 5. Security Scanning (security-scan)
**Purpose**: Identify security vulnerabilities
**Steps**:
- ✅ Trivy filesystem scanner
- ✅ SARIF results upload to GitHub Security

#### 6. Dependency Check (dependency-check)
**Purpose**: Check for vulnerable dependencies
**Steps**:
- ✅ Python dependency scanning (safety)
- ✅ Node.js dependency audit (npm audit)

#### 7. Performance Testing (performance-test)
**Purpose**: Verify performance standards
**Steps**:
- ✅ Load testing with Apache Bench
- ✅ Response time validation
- ✅ Failure rate monitoring

### Branch Protection Requirements

To enable branch protection, configure these requirements in GitHub:

```yaml
# Required status checks:
- Backend Tests & Quality
- Frontend Tests & Quality  
- Docker Build Verification
- End-to-End Tests

# Optional but recommended:
- Security Scanning
- Dependency Vulnerability Check
- Performance Testing
```

## Continuous Deployment (.github/workflows/release.yml)

### Trigger Events
- Version tags matching pattern `v*.*.*` (e.g., `v1.0.0`, `v2.1.3`)

### Version Tag Format
```bash
# Stable releases
git tag v1.0.0
git tag v1.2.3

# Pre-releases (marked as prerelease)
git tag v1.0.0-alpha.1
git tag v1.0.0-beta.2
git tag v1.0.0-rc.1
```

### Release Pipeline Jobs

#### 1. Extract Version Info (extract-version)
**Purpose**: Parse version information from git tag
**Outputs**:
- Version number (e.g., "1.2.3")
- Prerelease flag (true for alpha/beta/rc)

#### 2. Run CI Pipeline (run-ci)
**Purpose**: Execute full CI pipeline for release validation
**Reuses**: Complete CI workflow

#### 3. Build & Push Docker Images (build-and-push)
**Purpose**: Create and publish production Docker images
**Features**:
- ✅ Multi-architecture builds (linux/amd64, linux/arm64)
- ✅ Multiple tag formats (version, major.minor, major, latest)
- ✅ GitHub Container Registry (ghcr.io) publishing
- ✅ Build caching for performance

**Generated Images**:
```bash
ghcr.io/owner/repo-backend:v1.2.3
ghcr.io/owner/repo-backend:1.2
ghcr.io/owner/repo-backend:1
ghcr.io/owner/repo-backend:latest

ghcr.io/owner/repo-frontend:v1.2.3
ghcr.io/owner/repo-frontend:1.2
ghcr.io/owner/repo-frontend:1
ghcr.io/owner/repo-frontend:latest
```

#### 4. Build Release Artifacts (build-artifacts)
**Purpose**: Create downloadable release packages
**Artifacts**:
- Frontend build package (`wordmixr-frontend-X.X.X.tar.gz`)
- Backend source package (`wordmixr-backend-X.X.X.tar.gz`)
- Complete source package (`wordmixr-source-X.X.X.tar.gz`)
- SHA256 checksums (`checksums.sha256`)

#### 5. Security Scan Release (security-scan-release)
**Purpose**: Scan published Docker images for vulnerabilities
**Features**:
- ✅ Trivy container scanning
- ✅ SARIF results upload

#### 6. Generate Release Notes (generate-changelog)
**Purpose**: Auto-generate comprehensive release notes
**Content**:
- Git commit changelog
- Docker image references
- Quick start instructions
- Verification commands

#### 7. Create GitHub Release (create-release)
**Purpose**: Publish official GitHub release
**Features**:
- ✅ Automated release creation
- ✅ Attach all build artifacts
- ✅ Include generated release notes
- ✅ Mark pre-releases appropriately

#### 8. Performance Benchmark (performance-benchmark)
**Purpose**: Validate release performance
**Features**:
- ✅ Test with actual published Docker images
- ✅ Comprehensive load testing (1000 requests, 20 concurrent)
- ✅ Critical word scenario validation
- ✅ Performance report generation

#### 9. Deploy to Staging (deploy-staging)
**Purpose**: Automated staging deployment
**Features**:
- ✅ Only stable releases (not pre-releases)
- ✅ Environment protection
- ✅ Ready for production deployment customization

## Setup Instructions

### 1. Enable GitHub Actions
GitHub Actions are enabled by default for public repositories.

### 2. Configure Branch Protection
```bash
# Go to: Settings > Branches > Add rule

Branch name pattern: main (or master)

✅ Require a pull request before merging
✅ Require status checks to pass before merging
✅ Require branches to be up to date before merging

Required status checks:
- Backend Tests & Quality
- Frontend Tests & Quality
- Docker Build Verification  
- End-to-End Tests
```

### 3. Repository Secrets
No secrets required for basic operation. GitHub automatically provides:
- `GITHUB_TOKEN` for package publishing
- Workflow permissions for container registry

### 4. GitHub Packages Setup
Container images are automatically published to GitHub Container Registry (ghcr.io).

**Package Settings**:
1. Go to repository Packages
2. Connect packages to repository
3. Configure package visibility (public/private)

## Usage Examples

### Running CI on Pull Request
```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "Add new feature"

# 3. Push and create PR
git push origin feature/new-feature
# Create PR on GitHub

# CI automatically runs:
# ✅ All quality checks
# ✅ Tests (including critical word tests)
# ✅ Security scans
# ✅ Performance validation
```

### Creating a Release
```bash
# 1. Ensure main branch is ready
git checkout main
git pull origin main

# 2. Update CHANGELOG.md
# Add new version entry

# 3. Create and push version tag
git tag v1.2.3
git push origin v1.2.3

# Release pipeline automatically:
# 🚀 Runs full CI validation
# 🐳 Builds and publishes Docker images  
# 📦 Creates release artifacts
# 🔒 Security scans published images
# 📋 Generates release notes
# 🎉 Creates GitHub release
# 📊 Runs performance benchmarks
# 🚀 Deploys to staging (if configured)
```

### Using Released Images
```bash
# Pull and run specific version
docker run ghcr.io/owner/repo-backend:v1.2.3
docker run ghcr.io/owner/repo-frontend:v1.2.3

# Or use latest
docker run ghcr.io/owner/repo-backend:latest
docker run ghcr.io/owner/repo-frontend:latest

# Docker Compose with specific version
services:
  backend:
    image: ghcr.io/owner/repo-backend:v1.2.3
  frontend:
    image: ghcr.io/owner/repo-frontend:v1.2.3
```

## Monitoring and Troubleshooting

### Viewing Workflow Status
1. **Repository Actions Tab**: View all workflow runs
2. **PR Checks**: See status in pull request interface
3. **Commit Status**: Green checkmarks on commits

### Common CI Failures

#### Backend Test Failures
```bash
# Run locally to debug
cd backend
pytest tests/ -v
python -m black --check app/
python -m flake8 app/
```

#### Frontend Test Failures
```bash
# Run locally to debug
cd frontend
npm test
npm run lint
npm run type-check
```

#### Dictionary Quality Failures
Critical word tests fail when:
- Dictionary configuration changes
- Word coverage is reduced
- SCOWL Large not being used

**Fix**: Verify dictionary configuration and critical word presence

#### Performance Test Failures
Usually indicates:
- Response time > 500ms average
- High failure rate
- Memory/resource issues

### Release Troubleshooting

#### Docker Build Failures
- Check Dockerfile syntax
- Verify dependencies are available
- Check for architecture-specific issues

#### Container Registry Issues
- Verify GITHUB_TOKEN permissions
- Check package visibility settings
- Ensure repository packages are connected

### Performance Monitoring

#### Metrics Tracked
- **Response Time**: <50ms typical, <100ms p95
- **Throughput**: 100+ requests/second
- **Memory**: <1MB per request
- **Dictionary Load**: <200ms startup

#### Alerts
Performance tests fail if:
- Average response time > 500ms
- Any request failures occur
- Critical word scenarios fail

## Security Considerations

### Automated Security
- ✅ Dependency vulnerability scanning
- ✅ Container image scanning
- ✅ Code security analysis (bandit)
- ✅ SARIF results in GitHub Security tab

### Security Policy
1. **Dependencies**: Auto-scan and alert on vulnerabilities
2. **Images**: Scan before and after publishing
3. **Code**: Static analysis on every commit
4. **Access**: Minimal required permissions

## Future Enhancements

### Planned Improvements
1. **Deployment**: Add production deployment stage
2. **Notifications**: Slack/email integration
3. **Monitoring**: Add application performance monitoring
4. **Testing**: Expand browser-based E2E tests
5. **Metrics**: Add performance trend tracking

### Customization Options
1. **Environments**: Add development/staging/production
2. **Approvals**: Require manual approval for releases
3. **Rollback**: Implement automated rollback capability
4. **Scaling**: Add load testing with higher concurrency

This CI/CD pipeline ensures WordMixr maintains high quality, security, and performance standards while enabling rapid, reliable releases! 🎉 