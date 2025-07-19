# Dependabot Configuration 🤖

This document explains how Dependabot is configured for the WordMixr project to automatically manage dependency updates.

## 📋 **Overview**

Dependabot automatically scans your repository for outdated dependencies and creates pull requests to update them. It helps keep your project secure and up-to-date with the latest package versions.

## 🔧 **Configuration File**

The Dependabot configuration is defined in `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Frontend dependencies (npm)
  # Backend dependencies (Python pip)  
  # Docker dependencies
  # GitHub Actions dependencies
```

## 📦 **Package Ecosystems Monitored**

### **1. Frontend Dependencies (npm)**
- **Directory**: `/frontend`
- **Schedule**: Weekly on Mondays at 09:00 UTC
- **Dependencies**: React, TypeScript, Vite, testing libraries
- **Groups**: 
  - Development dependencies (TypeScript, ESLint, Prettier)
  - Production dependencies (React, Vite, Axios)

### **2. Backend Dependencies (Python pip)**
- **Directory**: `/backend`
- **Schedule**: Weekly on Mondays at 09:00 UTC
- **Dependencies**: FastAPI, Pydantic, testing libraries
- **Groups**:
  - FastAPI dependencies
  - Testing dependencies (pytest, coverage)
  - Linting dependencies (Black, isort, flake8)

### **3. Docker Dependencies**
- **Directories**: `/frontend` and `/backend`
- **Schedule**: Weekly on Mondays at 10:00 UTC
- **Dependencies**: Base images in Dockerfiles

### **4. GitHub Actions Dependencies**
- **Directory**: `/`
- **Schedule**: Weekly on Mondays at 11:00 UTC
- **Dependencies**: Action versions in workflow files

## ⚙️ **Configuration Features**

### **Pull Request Management**
- **Limits**: Maximum 2-5 open PRs per ecosystem
- **Auto-assignment**: PRs assigned to repository maintainers
- **Labeling**: Automatic labels for easy identification

### **Commit Messages**
- **Prefixes**: `frontend`, `backend`, `docker`, `ci`
- **Scope**: Includes dependency scope information
- **Development**: Special prefixes for dev dependencies

### **Dependency Grouping**
- **Related updates**: Groups similar dependencies together
- **Reduced noise**: Fewer individual PRs for related packages
- **Easier reviews**: Logical groupings for maintainers

## 🚀 **Getting Started**

### **1. Enable Dependabot**
Dependabot is automatically enabled when the configuration file is present in your repository.

### **2. Customize Configuration**
Replace `"tekenstam"` with your GitHub username in the configuration:

```yaml
reviewers:
  - "your-github-username"
assignees:
  - "your-github-username"
```

### **3. Review and Merge PRs**
- Review Dependabot PRs regularly
- Run tests to ensure compatibility
- Merge approved updates

## 📊 **Monitoring and Management**

### **Dependabot Dashboard**
- Access via GitHub repository "Insights" → "Dependency graph" → "Dependabot"
- View update status and schedules
- Monitor security vulnerabilities

### **Pull Request Review Process**
1. **Automated Testing**: CI runs on all Dependabot PRs
2. **Compatibility Check**: Ensure updates don't break functionality
3. **Security Review**: Check for known vulnerabilities
4. **Manual Testing**: Test critical functionality if needed

## 🔒 **Security Features**

### **Vulnerability Alerts**
- Automatic security updates for vulnerable dependencies
- Priority handling for critical security issues
- Integration with GitHub Security Advisories

### **Version Pinning**
- Dependabot respects semantic versioning
- Major version updates require manual approval
- Minor and patch updates can be auto-merged

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **PRs Not Created**
- Check if Dependabot is enabled in repository settings
- Verify configuration file syntax
- Ensure directories exist and contain dependency files

#### **Too Many PRs**
- Adjust `open-pull-requests-limit` values
- Use dependency grouping to reduce noise
- Consider changing update frequency

#### **Failed Updates**
- Review CI failures on Dependabot PRs
- Check for breaking changes in dependency updates
- Manually resolve conflicts if needed

### **Configuration Validation**
```bash
# Validate YAML syntax
yamllint .github/dependabot.yml

# Check Dependabot configuration
gh repo view --web  # Navigate to Insights → Dependency graph
```

## ⏰ **Schedule Summary**

| Ecosystem | Day | Time (UTC) | Frequency |
|-----------|-----|------------|-----------|
| Frontend (npm) | Monday | 09:00 | Weekly |
| Backend (pip) | Monday | 09:00 | Weekly |
| Docker (frontend) | Monday | 10:00 | Weekly |
| Docker (backend) | Monday | 10:00 | Weekly |
| GitHub Actions | Monday | 11:00 | Weekly |

## 🎯 **Best Practices**

### **For Maintainers**
- Review Dependabot PRs promptly
- Test updates in development environment
- Keep an eye on major version updates
- Monitor security advisories

### **For Contributors**
- Don't manually update dependencies that Dependabot manages
- Let Dependabot handle routine updates
- Focus on feature development and bug fixes

## 📚 **Related Documentation**

- [GitHub Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Dependabot Configuration Reference](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [WordMixr CI/CD Documentation](CICD.md)

---

Dependabot helps keep WordMixr secure and up-to-date automatically! 🚀 