# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with FastAPI
- Pre-commit hooks and linting configuration
- GitHub Actions CI/CD workflows
- Auto-release notes generation
- Commit message template and guidelines

### Changed
- Updated pyproject.toml with development dependencies

### Fixed
- Fixed .env configuration to match Settings schema
- Fixed linting issues in middleware and main files

## [0.1.0] - 2026-02-05

### Added
- FastAPI application structure
- Health check endpoint
- Middleware setup (Request ID, Logging, Rate Limiting)
- Configuration management with Pydantic Settings
- Docker and Docker Compose support
- Testing setup with pytest
- API versioning (v1, v2)
- Comprehensive documentation

### Security
- Added security scanning with Bandit and Safety
- Pre-commit hooks for security checks

---

*Generated releases will appear above this line*
