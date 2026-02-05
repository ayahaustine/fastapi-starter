#!/usr/bin/env python3
"""
Semantic Version Calculator
Analyzes commit messages and calculates the next version based on conventional commits.
"""

import re
import subprocess
import sys


def run_command(cmd: list) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def get_current_version() -> str:
    """Get current version from git tags or pyproject.toml."""
    # Try git tags first
    try:
        version = run_command(["git", "describe", "--tags", "--abbrev=0"])
        return version.lstrip("v")
    except:
        pass

    # Try pyproject.toml
    try:
        with open("pyproject.toml") as f:
            for line in f:
                if line.strip().startswith("version ="):
                    match = re.search(r'version = "([0-9]+\.[0-9]+\.[0-9]+)"', line)
                    if match:
                        return match.group(1)
    except FileNotFoundError:
        pass

    return "0.0.0"


def get_commits_since_last_tag() -> list:
    """Get commit messages since last tag."""
    try:
        last_tag = run_command(["git", "describe", "--tags", "--abbrev=0"])
        commits = run_command(["git", "log", f"{last_tag}..HEAD", "--pretty=format:%s"])
    except:
        # If no tags, get all commits
        commits = run_command(["git", "log", "--pretty=format:%s"])

    return [c for c in commits.split("\n") if c.strip()]


def parse_commit(commit_msg: str) -> tuple[str, bool]:
    """
    Parse a commit message and return (type, is_breaking).

    Returns:
        - type: feat, fix, docs, chore, etc.
        - is_breaking: True if contains BREAKING CHANGE
    """
    # Check for breaking change
    is_breaking = "BREAKING CHANGE" in commit_msg or "!" in commit_msg.split(":")[0]

    # Extract type
    type_match = re.match(
        r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+?\))?(!)?:",
        commit_msg,
    )

    if type_match:
        commit_type = type_match.group(1)
        return commit_type, is_breaking

    return "unknown", is_breaking


def calculate_next_version(current_version: str, commits: list) -> tuple[str, str]:
    """
    Calculate next version based on commits.

    Returns:
        - next_version: The calculated next version
        - bump_type: major, minor, or patch
    """
    parts = current_version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    has_breaking = False
    has_feature = False
    has_fix = False

    for commit in commits:
        commit_type, is_breaking = parse_commit(commit)

        if is_breaking:
            has_breaking = True
        elif commit_type == "feat":
            has_feature = True
        elif commit_type == "fix":
            has_fix = True

    # Determine bump type
    if has_breaking:
        major += 1
        minor = 0
        patch = 0
        bump_type = "major"
    elif has_feature:
        minor += 1
        patch = 0
        bump_type = "minor"
    elif has_fix:
        patch += 1
        bump_type = "patch"
    else:
        # No version bump needed
        return current_version, "none"

    next_version = f"{major}.{minor}.{patch}"
    return next_version, bump_type


def main():
    """Main function."""
    print("🔍 Analyzing commits for semantic versioning...")
    print()

    # Get current version
    current_version = get_current_version()
    print(f"📌 Current version: {current_version}")

    # Get commits since last tag
    commits = get_commits_since_last_tag()
    if not commits:
        print("⚠️  No commits found since last tag")
        print(f"✅ Version remains: {current_version}")
        print(current_version)  # For script parsing
        return

    print(f"📝 Analyzing {len(commits)} commit(s)...")
    print()

    # Analyze commits
    breaking_changes = []
    features = []
    fixes = []
    others = []

    for commit in commits:
        commit_type, is_breaking = parse_commit(commit)
        if is_breaking:
            breaking_changes.append(commit)
        elif commit_type == "feat":
            features.append(commit)
        elif commit_type == "fix":
            fixes.append(commit)
        else:
            others.append(commit)

    # Print summary
    if breaking_changes:
        print(f"💥 Breaking changes: {len(breaking_changes)}")
        for commit in breaking_changes[:3]:
            print(f"   - {commit[:80]}")
    if features:
        print(f"✨ Features: {len(features)}")
        for commit in features[:3]:
            print(f"   - {commit[:80]}")
    if fixes:
        print(f"🐛 Fixes: {len(fixes)}")
        for commit in fixes[:3]:
            print(f"   - {commit[:80]}")
    print()

    # Calculate next version
    next_version, bump_type = calculate_next_version(current_version, commits)

    if bump_type == "none":
        print("ℹ️  No version bump required")
        print(f"✅ Version remains: {current_version}")
        print(current_version)  # For script parsing
    else:
        print(f"📈 Bump type: {bump_type.upper()}")
        print(f"🎯 Next version: {next_version}")
        print()
        print(next_version)  # For script parsing


if __name__ == "__main__":
    main()
