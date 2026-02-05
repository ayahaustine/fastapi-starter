# Semantic Versioning Guide

This project uses [Semantic Versioning 2.0.0](https://semver.org/) with automated version calculation based on [Conventional Commits](https://www.conventionalcommits.org/).

## What is Semantic Versioning?

Given a version number `MAJOR.MINOR.PATCH`, increment:

- **MAJOR** version when you make incompatible API changes (breaking changes)
- **MINOR** version when you add functionality in a backward compatible manner (new features)
- **PATCH** version when you make backward compatible bug fixes

Example: `1.4.2` → `major.minor.patch`

## Automatic Version Calculation

The project includes tools to automatically calculate the next version based on your commit messages.

### Using the Semver Calculator

Check what the next version will be:

```bash
make semver
```

This analyzes your commits since the last tag and shows:
- Current version
- Breaking changes, features, and fixes
- Recommended version bump
- Next version number

### Automated Release

Create a release with automatic version detection:

```bash
make auto-release
```

This script will:
1. Analyze commits since last tag
2. Calculate next version automatically
3. Update version in `pyproject.toml`
4. Create git tag
5. Push to remote (with confirmation)

### Manual Release

If you prefer to specify the version manually:

```bash
make release VERSION=1.2.3
```

## Version Bump Rules

The semver calculator follows these rules:

| Commit Type | Example | Version Bump | Example Change |
|------------|---------|--------------|----------------|
| **BREAKING CHANGE** | `feat!: restructure API` | **MAJOR** | 1.2.3 → 2.0.0 |
| **feat:** | `feat: add user login` | **MINOR** | 1.2.3 → 1.3.0 |
| **fix:** | `fix: resolve null pointer` | **PATCH** | 1.2.3 → 1.2.4 |
| Other types | `docs:`, `chore:`, etc. | **NONE** | No bump |

### Breaking Changes

Breaking changes can be indicated in two ways:

```bash
# Method 1: Exclamation mark
git commit -m "feat!: change API response format"

# Method 2: Footer
git commit -m "refactor: restructure authentication

BREAKING CHANGE: Auth tokens now require 'Bearer' prefix
"
```

## Examples

### Scenario 1: Bug Fixes Only

**Commits since last tag (v1.2.3):**
```
fix(auth): resolve session timeout issue
fix(api): handle empty response gracefully
chore: update dependencies
```

**Result:** `1.2.3` → `1.2.4` (PATCH bump)

### Scenario 2: New Features

**Commits since last tag (v1.2.4):**
```
feat(api): add pagination support
feat(auth): implement refresh tokens
fix(database): optimize query performance
docs: update API documentation
```

**Result:** `1.2.4` → `1.3.0` (MINOR bump, ignores fixes)

### Scenario 3: Breaking Changes

**Commits since last tag (v1.3.0):**
```
feat!: change error response format

BREAKING CHANGE: All API errors now return standardized format
{ "error": { "code": "ERR_001", "message": "..." } }

fix(api): resolve validation bug
feat(ui): add dark mode
```

**Result:** `1.3.0` → `2.0.0` (MAJOR bump, ignores features/fixes)

### Scenario 4: No Version Bump

**Commits since last tag (v2.0.0):**
```
docs: update README
chore: update .gitignore
ci: improve workflow performance
style: format code
```

**Result:** `2.0.0` → `2.0.0` (NO bump)

## Workflow

### Recommended Release Process

1. **Develop with conventional commits**
   ```bash
   git commit -m "feat(api): add user export"
   git commit -m "fix(ui): resolve button alignment"
   ```

2. **Check what version will be next**
   ```bash
   make semver
   ```

3. **Review the output**
   ```
   🔍 Analyzing commits for semantic versioning...

   📌 Current version: 1.2.3
   📝 Analyzing 5 commit(s)...

   ✨ Features: 2
      - feat(api): add user export
      - feat(auth): implement 2FA
   🐛 Fixes: 1
      - fix(ui): resolve button alignment

   📈 Bump type: MINOR
   🎯 Next version: 1.3.0
   ```

4. **Create automated release**
   ```bash
   make auto-release
   ```

5. **Or create manual release**
   ```bash
   make release VERSION=1.3.0
   ```

## Pre-release Versions

For beta, alpha, or release candidate versions:

```bash
# Beta release
git tag v2.0.0-beta.1
git push origin v2.0.0-beta.1

# Release candidate
git tag v2.0.0-rc.1
git push origin v2.0.0-rc.1

# Alpha release
git tag v2.0.0-alpha.1
git push origin v2.0.0-alpha.1
```

Format: `{major}.{minor}.{patch}-{pre-release}.{number}`

## Version Precedence

Versions are compared in order:

```
1.0.0-alpha.1 < 1.0.0-alpha.2 < 1.0.0-beta.1 < 1.0.0-rc.1 < 1.0.0 < 1.0.1 < 1.1.0 < 2.0.0
```

## Initial Development

- Start with `0.1.0` for initial development
- Version `0.x.y` indicates the API is not stable
- Use `1.0.0` for the first stable release

## Version Metadata

You can add build metadata (doesn't affect version precedence):

```
1.0.0+20130313144700
1.0.0-beta.1+exp.sha.5114f85
```

## Best Practices

### 1. Never Modify Released Versions

Once a version is released, its contents MUST NOT be modified. Create a new version instead.

### 2. Document Breaking Changes

Always document breaking changes clearly:

```bash
git commit -m "refactor!: change configuration format

BREAKING CHANGE: Configuration now uses YAML instead of JSON.

Migration guide:
1. Convert config.json to config.yml
2. Update environment variables
3. Restart application
"
```

### 3. Group Related Changes

Try to group related changes in one commit:

```bash
# Good
git commit -m "feat(auth): add OAuth2 support

- Implement Google OAuth2
- Add Facebook OAuth2
- Update user model for OAuth data
"

# Less ideal (3 separate commits for related work)
git commit -m "feat: add Google OAuth2"
git commit -m "feat: add Facebook OAuth2"
git commit -m "feat: update user model"
```

### 4. Be Consistent

Use conventional commits consistently across the team.

## Troubleshooting

### Version Not Incrementing

If `make semver` shows no version bump:

- Check your commit messages follow conventional format
- Ensure commits contain `feat:`, `fix:`, or breaking changes
- Verify commits are after the last tag: `git log --oneline $(git describe --tags --abbrev=0)..HEAD`

### Wrong Version Calculated

The calculator prioritizes in this order:
1. Breaking changes (MAJOR)
2. Features (MINOR)
3. Fixes (PATCH)

If you have mixed commits, the highest priority change determines the bump.

### Manual Override

If you need a specific version regardless of commits:

```bash
make release VERSION=1.5.0
```

## Tools Used

- **scripts/semver.py**: Python script that analyzes commits
- **scripts/auto-release.sh**: Automated release script
- **GitHub Actions**: Automatic release notes generation

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Release Management Guide](release-management.md)
- [Commit Guidelines](commit-guidelines.md)
