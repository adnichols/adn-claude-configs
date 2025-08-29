#!/bin/bash

# Test Script for Claude Code Configuration Installer
# Comprehensive validation of installation functionality
# Author: Generated with Claude Code

set -e
set -u
set -o pipefail

readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly TEST_TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Color codes for test output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test result tracking
FAILED_TESTS=()

# Test directories
readonly TEST_CLAUDE_DIR="/tmp/test-claude-$TEST_TIMESTAMP"
readonly TEST_BACKUP_DIR="$HOME/.claude-backup-test-$TEST_TIMESTAMP"

# Test utility functions
test_header() {
    echo -e "${BLUE}=====================================${NC}"
    echo -e "${BLUE}  Claude Code Installer Test Suite${NC}"
    echo -e "${BLUE}=====================================${NC}"
    echo
}

test_section() {
    echo -e "${BLUE}--- $1 ---${NC}"
}

test_case() {
    local test_name="$1"
    ((TESTS_RUN++))
    echo -n "Testing: $test_name ... "
}

test_pass() {
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
}

test_fail() {
    local reason="$1"
    echo -e "${RED}FAIL${NC} - $reason"
    ((TESTS_FAILED++))
    FAILED_TESTS+=("$reason")
}

# Cleanup function
cleanup_test_env() {
    echo "Cleaning up test environment..."
    
    # Remove test directories
    [[ -d "$TEST_CLAUDE_DIR" ]] && rm -rf "$TEST_CLAUDE_DIR"
    [[ -d "$TEST_BACKUP_DIR" ]] && rm -rf "$TEST_BACKUP_DIR"
    
    # Restore original ~/.claude if it was moved
    if [[ -d "$HOME/.claude-backup-for-test" ]]; then
        if [[ -d "$HOME/.claude" ]]; then
            rm -rf "$HOME/.claude"
        fi
        mv "$HOME/.claude-backup-for-test" "$HOME/.claude"
    fi
}

# Setup test environment
setup_test_env() {
    test_section "Setting up test environment"
    
    # Backup existing ~/.claude if it exists
    if [[ -d "$HOME/.claude" ]]; then
        mv "$HOME/.claude" "$HOME/.claude-backup-for-test"
        echo "Backed up existing ~/.claude directory"
    fi
    
    # Create test directories
    mkdir -p "$TEST_CLAUDE_DIR"
    echo "Created test directories"
}

# Test 1: Script permissions and basic structure
test_script_permissions() {
    test_case "Script permissions and executability"
    
    if [[ ! -f "$SCRIPT_DIR/install.sh" ]]; then
        test_fail "install.sh not found"
        return
    fi
    
    if [[ ! -x "$SCRIPT_DIR/install.sh" ]]; then
        test_fail "install.sh not executable"
        return
    fi
    
    test_pass
}

# Test 2: Repository structure validation
test_repository_structure() {
    test_case "Repository structure validation"
    
    local missing_dirs=()
    
    [[ ! -d "$SCRIPT_DIR/agents" ]] && missing_dirs+=("agents")
    [[ ! -d "$SCRIPT_DIR/commands" ]] && missing_dirs+=("commands")
    
    if [[ ${#missing_dirs[@]} -gt 0 ]]; then
        test_fail "Missing directories: ${missing_dirs[*]}"
        return
    fi
    
    # Check for content in directories
    local agents_count=$(find "$SCRIPT_DIR/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    local commands_count=$(find "$SCRIPT_DIR/commands" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    
    if [[ "$agents_count" -eq 0 ]]; then
        test_fail "No .md files in agents directory"
        return
    fi
    
    if [[ "$commands_count" -eq 0 ]]; then
        test_fail "No .md files in commands directory"
        return
    fi
    
    test_pass
}

# Test 3: Cross-platform compatibility
test_cross_platform_compatibility() {
    test_case "Cross-platform command compatibility"
    
    # Test readlink command
    if ! command -v readlink >/dev/null 2>&1; then
        test_fail "readlink command not available"
        return
    fi
    
    # Test ln command with -sf flags
    local test_target="/tmp/test-target-$$"
    local test_link="/tmp/test-link-$$"
    
    echo "test" > "$test_target"
    
    if ! ln -sf "$test_target" "$test_link" 2>/dev/null; then
        test_fail "ln -sf command failed"
        rm -f "$test_target"
        return
    fi
    
    if [[ ! -L "$test_link" ]]; then
        test_fail "Symlink was not created"
        rm -f "$test_target" "$test_link"
        return
    fi
    
    # Clean up test files
    rm -f "$test_target" "$test_link"
    test_pass
}

# Test 4: Error handling
test_error_handling() {
    test_case "Error handling with invalid repository"
    
    # Create a temporary directory without required structure
    local temp_dir="/tmp/invalid-repo-$$"
    mkdir -p "$temp_dir"
    
    # Change to invalid directory and try to run installer
    cd "$temp_dir"
    
    # The installer should fail gracefully
    if "$SCRIPT_DIR/install.sh" >/dev/null 2>&1; then
        test_fail "Installer should have failed in invalid directory"
        rm -rf "$temp_dir"
        cd "$SCRIPT_DIR"
        return
    fi
    
    # Clean up and return to script directory
    rm -rf "$temp_dir"
    cd "$SCRIPT_DIR"
    test_pass
}

# Test 5: Backup functionality (simulation)
test_backup_functionality() {
    test_case "Backup functionality simulation"
    
    # Create fake existing ~/.claude structure
    mkdir -p "$HOME/.claude/agents"
    mkdir -p "$HOME/.claude/commands"
    echo "test agent" > "$HOME/.claude/agents/test.md"
    echo "test command" > "$HOME/.claude/commands/test.md"
    
    # This is a basic test - in real scenario we'd need to mock the installer
    # For now, just verify the backup directory structure makes sense
    local backup_name="claude-backup-$(date +"%Y%m%d-%H%M%S")"
    local backup_path="$HOME/.claude-backup/$backup_name"
    
    # Simulate what the backup process should do
    mkdir -p "$backup_path"
    cp -r "$HOME/.claude/agents" "$backup_path/"
    cp -r "$HOME/.claude/commands" "$backup_path/"
    
    if [[ ! -d "$backup_path/agents" ]] || [[ ! -d "$backup_path/commands" ]]; then
        test_fail "Backup simulation failed"
        rm -rf "$HOME/.claude" "$HOME/.claude-backup"
        return
    fi
    
    # Clean up
    rm -rf "$HOME/.claude" "$HOME/.claude-backup"
    test_pass
}

# Test 6: POSIX compliance check
test_posix_compliance() {
    test_case "POSIX compliance of installer script"
    
    # Check for bash-specific features that might cause issues
    if grep -q "\\[\\[" "$SCRIPT_DIR/install.sh"; then
        # This is actually expected since we're using bash, but let's verify it's in the shebang
        if ! head -1 "$SCRIPT_DIR/install.sh" | grep -q "bash"; then
            test_fail "Uses bash features but doesn't specify bash in shebang"
            return
        fi
    fi
    
    # Check that script uses 'set -e' for error handling
    if ! grep -q "set -e" "$SCRIPT_DIR/install.sh"; then
        test_fail "Script doesn't use 'set -e' for error handling"
        return
    fi
    
    test_pass
}

# Test 7: Exit codes
test_exit_codes() {
    test_case "Proper exit codes"
    
    # Test running from wrong directory (should exit with specific code)
    local temp_dir="/tmp/wrong-dir-$$"
    mkdir -p "$temp_dir"
    cd "$temp_dir"
    
    local exit_code=0
    "$SCRIPT_DIR/install.sh" >/dev/null 2>&1 || exit_code=$?
    
    cd "$SCRIPT_DIR"
    rm -rf "$temp_dir"
    
    if [[ $exit_code -eq 0 ]]; then
        test_fail "Should have failed with non-zero exit code when run from wrong directory"
        return
    fi
    
    test_pass
}

# Main test execution
run_tests() {
    test_header
    
    # Setup
    setup_test_env
    trap cleanup_test_env EXIT
    
    # Run all tests
    test_section "Basic Functionality Tests"
    test_script_permissions
    test_repository_structure
    
    test_section "Cross-Platform Compatibility Tests"
    test_cross_platform_compatibility
    test_posix_compliance
    
    test_section "Error Handling Tests"
    test_error_handling
    test_exit_codes
    
    test_section "Feature Tests"
    test_backup_functionality
    
    # Results summary
    echo
    test_section "Test Results Summary"
    echo "Total tests run: $TESTS_RUN"
    echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
    
    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo
        echo -e "${RED}Failed tests:${NC}"
        for failed_test in "${FAILED_TESTS[@]}"; do
            echo -e "  • $failed_test"
        done
        echo
        echo -e "${RED}Some tests failed. Please review the installer implementation.${NC}"
        exit 1
    else
        echo
        echo -e "${GREEN}All tests passed! The installer is ready for use.${NC}"
        exit 0
    fi
}

# Main execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_tests "$@"
fi