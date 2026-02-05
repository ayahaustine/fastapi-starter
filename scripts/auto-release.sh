#!/bin/bash

# Automated Semantic Release Script
# Analyzes commits and automatically determines the next version

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error() {
    echo -e "${RED}❌ Error: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if working directory is clean
check_git_status() {
    if [[ -n $(git status -s) ]]; then
        print_error "Working directory is not clean. Commit or stash your changes first."
        exit 1
    fi
}

# Update version in pyproject.toml
update_version_files() {
    local version=$1

    if [[ -f "pyproject.toml" ]]; then
        sed -i.bak -E "s/^version = \"[0-9]+\.[0-9]+\.[0-9]+\"/version = \"${version}\"/" pyproject.toml
        rm pyproject.toml.bak
        print_success "Updated version in pyproject.toml"
    fi
}

main() {
    print_info "🚀 Automated Semantic Release"
    echo ""

    # Check git status
    print_info "Checking git status..."
    check_git_status

    # Calculate next version using Python script
    print_info "Calculating next version based on commits..."
    echo ""

    # Run semver calculator and capture output
    VERSION_OUTPUT=$(python3 scripts/semver.py)

    # Extract the version (last line of output)
    NEXT_VERSION=$(echo "$VERSION_OUTPUT" | tail -n 1)

    # Show full output
    echo "$VERSION_OUTPUT" | head -n -1

    # Check if version changed
    CURRENT_VERSION=$(echo "$VERSION_OUTPUT" | grep "Current version:" | awk '{print $4}')

    if [[ "$NEXT_VERSION" == "$CURRENT_VERSION" ]]; then
        print_warning "No version bump needed. Exiting."
        exit 0
    fi

    echo ""
    print_info "Proposed version: v$NEXT_VERSION"
    echo ""

    # Confirm release
    read -p "Create release v$NEXT_VERSION? (y/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Release cancelled"
        exit 0
    fi

    # Update version files
    print_info "Updating version files..."
    update_version_files "$NEXT_VERSION"

    # Commit version bump
    git add pyproject.toml
    git commit -m "chore: bump version to $NEXT_VERSION"
    print_success "Version bump committed"

    # Create tag
    git tag -a "v$NEXT_VERSION" -m "Release v$NEXT_VERSION"
    print_success "Tag v$NEXT_VERSION created"

    echo ""
    read -p "Push to remote and trigger release? (y/N): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin main
        git push origin "v$NEXT_VERSION"
        print_success "Pushed to remote!"
        echo ""
        print_success "🎉 Release v$NEXT_VERSION created!"
        print_info "GitHub Actions will generate release notes automatically"
        print_info "View at: https://github.com/$(git config remote.origin.url | sed -E 's/.*[:/](.*)\.git/\1/')/releases"
    else
        print_warning "Not pushed to remote"
        print_info "To push manually, run:"
        print_info "  git push origin main"
        print_info "  git push origin v$NEXT_VERSION"
    fi
}

main "$@"
