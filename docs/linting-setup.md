# Code Quality & Pre-commit Setup

This project uses pre-commit hooks and automated linting to maintain code quality.

## Tools Used

- **Ruff**: Fast Python linter and formatter (replaces Black, isort, flake8, and more)
- **MyPy**: Static type checker for Python
- **Pre-commit**: Git hook framework for running checks before commits

## Installation

Install all development dependencies including linting tools:

```bash
make dev-install
```

Or manually:

```bash
pip install -e ".[dev]"
pre-commit install
```

## Usage

### Running Linters

```bash
# Run all linting checks
make lint

# Auto-format code and fix linting issues
make format

# Run type checking
make type-check

# Run all checks via pre-commit
make pre-commit-run
```

### Manual Commands

```bash
# Ruff linting
ruff check .                    # Check for issues
ruff check . --fix              # Fix issues automatically

# Ruff formatting
ruff format .                   # Format all files

# MyPy type checking
mypy app/                       # Type check the app directory

# Pre-commit
pre-commit run --all-files      # Run all hooks on all files
pre-commit run --files app/main.py  # Run hooks on specific files
```

### Using the Lint Script

```bash
./scripts/lint.sh
```

This script runs:
1. Ruff linter with auto-fix
2. Ruff formatter
3. MyPy type checker

## Pre-commit Hooks

Pre-commit hooks run automatically before each commit. They include:

### General File Checks
- Trailing whitespace removal
- End-of-file fixing
- YAML/JSON/TOML syntax validation
- Large file detection (>1MB)
- Merge conflict detection
- Private key detection
- Mixed line ending normalization

### Python-Specific Checks
- **Ruff Linter**: Catches bugs, enforces style, and improves code quality
- **Ruff Formatter**: Formats code consistently
- **MyPy**: Type checking for better code reliability

## Configuration

### Ruff Configuration

Ruff is configured in [pyproject.toml](pyproject.toml) and [.ruff.toml](.ruff.toml):

- **Line length**: 100 characters
- **Target Python**: 3.13
- **Enabled rules**:
  - E, W: pycodestyle errors and warnings
  - F: pyflakes
  - I: isort (import sorting)
  - B: flake8-bugbear
  - C4: flake8-comprehensions
  - UP: pyupgrade
  - ARG: flake8-unused-arguments
  - SIM: flake8-simplify
  - PTH: flake8-use-pathlib
  - PL: pylint

### MyPy Configuration

MyPy is configured in [pyproject.toml](pyproject.toml):

- Type checking with Pydantic plugin
- Strict equality checks
- Redundant cast warnings
- No implicit optionals

### Pre-commit Configuration

Pre-commit is configured in [.pre-commit-config.yaml](.pre-commit-config.yaml).

To update hook versions:

```bash
pre-commit autoupdate
```

## Skipping Hooks

If you need to skip pre-commit hooks (not recommended):

```bash
git commit --no-verify
```

## CI/CD Integration

These linting checks should be integrated into your CI/CD pipeline. Add to your CI config:

```yaml
- name: Run linters
  run: |
    pip install -e ".[dev]"
    ruff check .
    ruff format --check .
    mypy app/
```

## Editor Integration

### VS Code

Install these extensions for real-time linting:
- Ruff (charliermarsh.ruff)
- Pylance (ms-python.vscode-pylance)
- MyPy Type Checker (ms-python.mypy-type-checker)

Add to `.vscode/settings.json`:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "ruff.lint.args": ["--config=.ruff.toml"],
  "python.linting.enabled": true
}
```

### PyCharm

1. Go to **Settings → Tools → External Tools**
2. Add Ruff as an external tool
3. Configure file watcher for automatic formatting

## Troubleshooting

### Pre-commit hooks not running

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
```

### Linting errors

```bash
# See detailed error messages
ruff check . --show-source

# Fix all auto-fixable issues
ruff check . --fix
```

### Type checking errors

```bash
# Run with verbose output
mypy app/ --verbose

# Ignore specific modules
mypy app/ --ignore-missing-imports
```

## Best Practices

1. **Run linters before committing**: Use `make format` or let pre-commit handle it
2. **Keep hooks updated**: Run `pre-commit autoupdate` monthly
3. **Don't bypass hooks**: Fix issues rather than using `--no-verify`
4. **Type hints**: Add type hints to new functions for better type checking
5. **Review auto-fixes**: Always review what auto-formatters change before committing
