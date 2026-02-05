# Release Management

This guide covers the release process and automated release notes generation.

## Quick Start

### Setup Commit Template

Configure git to use the commit message template:

```bash
make setup-git
```

This sets up the [.gitmessage](.gitmessage) template that helps you write conventional commits.

### Creating a Release

#### Option 1: Using Makefile

```bash
# Create and push a new version tag
make release VERSION=1.0.0
```

#### Option 2: Using Release Script

```bash
# Automatically bump version and create release
./scripts/release.sh patch   # 1.0.0 → 1.0.1
./scripts/release.sh minor   # 1.0.0 → 1.1.0
./scripts/release.sh major   # 1.0.0 → 2.0.0
```

#### Option 3: Manual Process

```bash
# Update version in pyproject.toml
# Commit the change
git add pyproject.toml
git commit -m "chore: bump version to 1.0.0"

# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0
```

## Conventional Commits

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- **feat**: New feature (triggers minor version bump)
- **fix**: Bug fix (triggers patch version bump)
- **docs**: Documentation changes
- **style**: Code style/formatting
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Test updates
- **build**: Build system changes
- **ci**: CI/CD changes
- **chore**: Maintenance tasks

### Examples

```bash
# Feature
git commit -m "feat(auth): add JWT token refresh endpoint"

# Bug fix
git commit -m "fix(api): handle null response in user endpoint"

# Breaking change
git commit -m "refactor(api)!: restructure error response format

BREAKING CHANGE: Error response format has changed.
Old: { error: 'message' }
New: { message: 'error message', code: 'ERROR_CODE' }
"
```

## Automated Release Notes

When you push a version tag (e.g., `v1.0.0`), the [release workflow](.github/workflows/release.yml) automatically:

1. **Generates changelog** from commit messages
2. **Categorizes changes** by type:
   - ✨ Features
   - 🐛 Bug Fixes
   - 📝 Documentation
   - ⚡ Performance
   - ♻️ Refactoring
   - 🚀 CI/CD
   - 💥 Breaking Changes
3. **Lists contributors**
4. **Creates GitHub release** with notes
5. **Updates CHANGELOG.md**

### Changelog Categories

The release notes are automatically organized into:

| Category | Commits Included | Icon |
|----------|-----------------|------|
| Features | `feat:` | ✨ |
| Bug Fixes | `fix:` | 🐛 |
| Documentation | `docs:` | 📝 |
| Performance | `perf:` | ⚡ |
| Refactoring | `refactor:` | ♻️ |
| CI/CD | `ci:`, `build:` | 🚀 |
| Breaking Changes | `BREAKING CHANGE:` | 💥 |

## Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

### Version Bumping Rules

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `fix:` | Patch | 1.0.0 → 1.0.1 |
| `feat:` | Minor | 1.0.0 → 1.1.0 |
| `BREAKING CHANGE:` | Major | 1.0.0 → 2.0.0 |
| `docs:`, `style:`, `refactor:`, `perf:`, `test:` | None | - |

## Pre-release Versions

For testing before official release:

```bash
# Create pre-release tag
git tag -a v1.0.0-rc.1 -m "Release candidate 1"
git push origin v1.0.0-rc.1

# Or beta version
git tag -a v1.0.0-beta.1 -m "Beta release 1"
git push origin v1.0.0-beta.1
```

## Manual Release Notes Editing

After automatic generation, you can edit release notes:

1. Go to [Releases](https://github.com/YOUR_REPO/releases)
2. Click on the release
3. Click "Edit release"
4. Modify the notes
5. Save changes

## CHANGELOG.md

The [CHANGELOG.md](../CHANGELOG.md) is automatically updated with each release. You can also update it manually following the [Keep a Changelog](https://keepachangelog.com/) format.

### Manual Changelog Update

```bash
# Generate changelog (requires git-chglog)
make changelog

# Or install git-chglog
brew install git-chglog
```

## Commit Message Validation

Pull requests are automatically validated for conventional commit format:

- ✅ PR title must follow conventional format
- ✅ All commits in PR must follow conventional format
- ✅ Commit messages are checked in CI

### Validation Workflow

The [commitlint workflow](.github/workflows/commitlint.yml) runs on every PR to ensure commits follow the convention.

## Best Practices

### Writing Good Commit Messages

1. **Use imperative mood**: "add" not "added" or "adds"
2. **Be specific**: "fix login redirect loop" not "fix bug"
3. **Reference issues**: "Fixes #123" or "Closes #456"
4. **Explain why**: Include body text for complex changes
5. **One concern per commit**: Split unrelated changes

### Release Checklist

Before creating a release:

- [ ] All tests pass locally (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is reviewed
- [ ] Breaking changes are documented
- [ ] Migration guide included (if needed)

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `fix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes

## Tools

### Commitizen (Optional)

For interactive commit creation:

```bash
pip install commitizen
cz commit
```

### git-chglog (Optional)

For advanced changelog generation:

```bash
brew install git-chglog

# Generate changelog
git-chglog -o CHANGELOG.md
```

## Troubleshooting

### Tag Already Exists

```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0

# Create tag again
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Release Workflow Failed

Check [Actions](https://github.com/YOUR_REPO/actions) tab for error details. Common issues:

- Missing permissions for `GITHUB_TOKEN`
- Invalid tag format
- Git history issues

### Commit Validation Failing

Ensure your commits follow the conventional format:

```bash
# Bad
git commit -m "fixed bug"

# Good
git commit -m "fix(api): resolve null pointer exception in user endpoint"
```

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Commit Guidelines](commit-guidelines.md)
