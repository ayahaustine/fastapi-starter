#!/bin/bash

# Release Helper Script
# Usage: ./scripts/release.sh [major|minor|patch]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
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

# Check if git is clean
check_git_status() {
    if [[ -n $(git status -s) ]]; then
        print_error "Working directory is not clean. Commit or stash your changes first."
        exit 1
    fi
}

# Get current version
get_current_version() {
    # Try to get from pyproject.toml
    if [[ -f "pyproject.toml" ]]; then
        CURRENT_VERSION=$(grep -E '^version = "[0-9]+\.[0-9]+\.[0-9]+"' pyproject.toml | sed -E 's/version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/')
    fi

    # Fallback to latest git tag
    if [[ -z "$CURRENT_VERSION" ]]; then
        CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//' || echo "0.0.0")
    fi

    echo "$CURRENT_VERSION"
}

# Calculate next version
calculate_next_version() {
    local version=$1
    local bump_type=$2

    IFS='.' read -r -a version_parts <<< "$version"
    local major="${version_parts[0]}"
    local minor="${version_parts[1]}"
    local patch="${version_parts[2]}"

    case $bump_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            print_error "Invalid bump type: $bump_type. Use: major, minor, or patch"
            exit 1
            ;;
    esac

    echo "${major}.${minor}.${patch}"
}

# Update version in pyproject.toml
update_pyproject_version() {
    local new_version=$1

    if [[ -f "pyproject.toml" ]]; then
        sed -i.bak -E "s/^version = \"[0-9]+\.[0-9]+\.[0-9]+\"/version = \"${new_version}\"/" pyproject.toml
        rm pyproject.toml.bak
        print_success "Updated version in pyproject.toml"
    fi
}

# Main script
main() {
    print_info "FastAPI Starter Release Helper"
    echo ""

    # Check arguments
    if [[ $# -eq 0 ]]; then
        print_error "Missing argument. Usage: ./scripts/release.sh [major|minor|patch]"
        exit 1
    fi

    BUMP_TYPE=$1

    # Validate bump type
    if [[ ! "$BUMP_TYPE" =~ ^(major|minor|patch)$ ]]; then
        print_error "Invalid bump type: $BUMP_TYPE. Use: major, minor, or patch"
        exit 1
    fi

    # Check git status
    check_git_status

    # Get current version
    CURRENT_VERSION=$(get_current_version)
    print_info "Current version: $CURRENT_VERSION"

    # Calculate next version
    NEXT_VERSION=$(calculate_next_version "$CURRENT_VERSION" "$BUMP_TYPE")
    print_info "Next version: $NEXT_VERSION"

    # Confirm
    echo ""
    read -p "Create release v$NEXT_VERSION? (y/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Release cancelled"
        exit 0
    fi

    # Update version in files
    print_info "Updating version in files..."
    update_pyproject_version "$NEXT_VERSION"

    # Commit version update
    git add pyproject.toml
    git commit -m "chore: bump version to $NEXT_VERSION"
    print_success "Version update committed"

    # Create tag
    git tag -a "v$NEXT_VERSION" -m "Release v$NEXT_VERSION"
    print_success "Tag v$NEXT_VERSION created"

    # Push
    echo ""
    read -p "Push to remote? (y/N): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin main
        git push origin "v$NEXT_VERSION"
        print_success "Pushed to remote"
        echo ""
        print_success "Release v$NEXT_VERSION created successfully!"
        print_info "GitHub Actions will automatically generate release notes"
        print_info "View at: https://github.com/$(git config remote.origin.url | sed -E 's/.*[:/](.*)\.git/\1/')/releases"
    else
        print_warning "Not pushed to remote"
        print_info "To push manually, run:"
        print_info "  git push origin main"
        print_info "  git push origin v$NEXT_VERSION"
    fi
}

# Run main
main "$@"
