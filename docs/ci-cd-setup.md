# CI/CD Pipeline Documentation

This project uses GitHub Actions for continuous integration and deployment.

## Workflows

### 1. CI Pipeline ([ci.yml](.github/workflows/ci.yml))

**Triggers**: Push and PR to `main` or `develop` branches

**Jobs**:

#### Lint & Format Check
- Runs Ruff linter to check code quality
- Verifies code formatting with Ruff
- Runs MyPy type checker (non-blocking)

#### Test
- Runs on Python 3.13
- Executes all pytest tests
- Uploads coverage to Codecov
- Matrix strategy allows testing multiple Python versions

#### Security Scan
- Runs `safety` to check for vulnerable dependencies
- Runs `bandit` for security issues in code
- Both checks are non-blocking (informational)

#### Build & Validate
- Validates package can be built
- Tests that the app can be imported successfully
- Only runs if lint and test jobs pass

#### Docker Build
- Builds Docker image to verify Dockerfile
- Uses layer caching for faster builds
- Does not push the image (test only)
- Only runs if lint and test jobs pass

### 2. Pre-commit Checks ([pre-commit.yml](.github/workflows/pre-commit.yml))

**Triggers**: Pull requests to `main` or `develop`

**Purpose**: Runs all pre-commit hooks on the entire codebase

**Checks**:
- Trailing whitespace
- End-of-file fixing
- YAML/JSON/TOML validation
- Large file detection
- Merge conflict detection
- Private key detection
- Code formatting and linting

### 3. Code Coverage ([coverage.yml](.github/workflows/coverage.yml))

**Triggers**: Push to `main` or PRs to `main`

**Purpose**: Generate and track code coverage

**Features**:
- Generates coverage reports (XML, HTML, terminal)
- Uploads to Codecov
- Creates coverage artifacts for download
- Posts coverage comments on PRs
- Minimum coverage thresholds: 80% green, 60% orange

### 4. Dependency Updates ([dependencies.yml](.github/workflows/dependencies.yml))

**Triggers**:
- Weekly schedule (Mondays at 9:00 AM UTC)
- Manual workflow dispatch

**Purpose**: Automated dependency security and update checks

**Actions**:
- Lists outdated packages
- Runs security audit with `pip-audit`
- Creates GitHub issues for review


## Setup Instructions

### 1. Enable GitHub Actions

Ensure Actions are enabled in your repository settings:
`Settings → Actions → General → Allow all actions`

### 2. Configure Environments

For production deployments, create environments:

1. Go to `Settings → Environments`
2. Create `staging` and `production` environments
3. Add protection rules:
   - Required reviewers for production
   - Wait timer before deployment
   - Limit which branches can deploy

### 3. Branch Protection Rules

Recommended settings for `main` branch:

1. `Settings → Branches → Add rule`
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
     - Select: `lint`, `test`, `pre-commit`
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings

## Status Badges

Add these badges to your README.md:

```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/badge.svg)
![Pre-commit](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Pre-commit%20Checks/badge.svg)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO)
```

## Local Testing

Test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act

# Run CI workflow
act -j lint
act -j test

# Run all workflows
act push
```

## Workflow Optimization

### Caching

All workflows use caching to speed up runs:
- **pip cache**: Cached by `actions/setup-python@v5`
- **pre-commit cache**: Explicitly cached in pre-commit workflow
- **Docker layers**: Cached using GitHub Actions cache

### Matrix Strategy

The test job can be expanded to test multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
```

### Concurrency Control

Prevent multiple workflow runs:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Monitoring & Debugging

### View Workflow Runs

1. Go to `Actions` tab in your repository
2. Click on a workflow run to see details
3. Click on a job to see logs

### Debug Mode

Enable debug logging:

1. `Settings → Secrets → New repository secret`
2. Name: `ACTIONS_STEP_DEBUG`
3. Value: `true`

### Re-run Failed Jobs

Click "Re-run failed jobs" or "Re-run all jobs" in the workflow run page.

## Best Practices

1. **Keep workflows fast**: Use caching, parallelization
2. **Fail fast**: Critical checks should fail the build
3. **Security first**: Never log secrets, use secret scanning
4. **Test locally**: Use pre-commit hooks and act
5. **Monitor costs**: GitHub Actions has usage limits
6. **Review regularly**: Update actions versions monthly

## Troubleshooting

### Workflow Not Triggering

- Check branch names in workflow triggers
- Verify workflow file syntax with YAML linter
- Ensure Actions are enabled for the repository

### Tests Failing in CI but Passing Locally

- Check Python version compatibility
- Verify environment variables are set
- Review differences in OS (Linux vs macOS/Windows)

### Docker Build Failures

- Test Dockerfile locally: `docker build -t test .`
- Check for missing files in `.dockerignore`
- Verify base image is accessible

### Permission Errors

- Check repository settings for Actions permissions
- Verify `GITHUB_TOKEN` has necessary scopes
- For deployments, ensure secrets are properly configured

## Further Reading

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
