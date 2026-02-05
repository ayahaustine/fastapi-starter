# Commit Message Guidelines

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Setup Git Commit Template

To use the commit message template automatically:

```bash
git config commit.template .gitmessage
```

Or for this repository only:

```bash
git config --local commit.template .gitmessage
```

## Types

| Type | Description | Example |
|------|-------------|---------|
| **feat** | New feature | `feat(auth): add JWT token refresh` |
| **fix** | Bug fix | `fix(api): handle null response in user endpoint` |
| **docs** | Documentation changes | `docs: update API examples in README` |
| **style** | Code style/formatting | `style: format code with black` |
| **refactor** | Code refactoring | `refactor(database): simplify query logic` |
| **perf** | Performance improvements | `perf(api): optimize database queries` |
| **test** | Adding/updating tests | `test: add unit tests for auth service` |
| **build** | Build system changes | `build: update dependencies` |
| **ci** | CI/CD changes | `ci: add coverage reporting to workflow` |
| **chore** | Maintenance tasks | `chore: update .gitignore` |
| **revert** | Revert previous commit | `revert: feat(auth): add JWT token refresh` |

## Scope (Optional)

The scope provides additional context about what part of the codebase is affected:

- `auth` - Authentication/authorization
- `api` - API endpoints
- `database` - Database operations
- `middleware` - Middleware functions
- `config` - Configuration
- `tests` - Test files
- `docs` - Documentation
- `ci` - CI/CD workflows

## Subject

The subject contains a succinct description of the change:

- Use the **imperative mood**: "add" not "added" or "adds"
- Don't capitalize the first letter
- No period (.) at the end
- Limit to **50 characters**

## Body (Optional)

The body should include the motivation for the change and contrast this with previous behavior:

- Wrap at **72 characters**
- Explain **what** and **why**, not **how**
- Use imperative mood
- Can include multiple paragraphs

## Footer (Optional)

The footer should contain:

### Issue References
```
Fixes #123
Closes #456
Refs #789
```

### Breaking Changes
```
BREAKING CHANGE: description of what broke and migration instructions
```

## Examples

### Simple Feature
```
feat(auth): add password reset functionality
```

### Bug Fix with Details
```
fix(database): resolve connection pool exhaustion

The connection pool was not being properly released after
queries, leading to connection exhaustion under high load.
Added explicit connection cleanup in finally blocks.

Fixes #234
```

### Breaking Change
```
refactor(api): restructure error response format

BREAKING CHANGE: Error responses now use a standardized format.
Old format: { error: "message" }
New format: { message: "error message", code: "ERROR_CODE", details: {} }

Closes #145
```

### Documentation Update
```
docs: add deployment guide for production

Added comprehensive documentation covering:
- Environment configuration
- Docker deployment
- Database migrations
- Monitoring setup
```

### Multiple Issues
```
feat(api): add batch processing endpoint

Implements batch processing for multiple resources in a single
request. Improves performance by reducing HTTP overhead.

Implements #123
Closes #124
Refs #125
```

## Benefits

Following these conventions enables:

- **Automated changelog generation**
- **Automatic semantic versioning**
- **Better navigation of git history**
- **Clear communication in code reviews**
- **Easier collaboration**

## Validation

Commits are validated using pre-commit hooks and CI/CD pipelines to ensure they follow the conventional format.

## Tools

### Commitizen

For interactive commit message creation:

```bash
pip install commitizen
cz commit
```

### Commitlint

For validating commit messages:

```bash
npm install -g @commitlint/cli @commitlint/config-conventional
```

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org/)
