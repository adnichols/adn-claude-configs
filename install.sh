#!/bin/bash

# Claude Code Configuration Installer
# Installs custom agents and commands by creating symlinks from ~/.claude to this repository
# Author: Generated with Claude Code

set -e  # Exit on any command failure
set -u  # Exit on undefined variables
set -o pipefail  # Exit on pipe failures

# Script version and metadata
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_INVALID_LOCATION=1
readonly EXIT_INVALID_REPO=2
readonly EXIT_BACKUP_FAILED=3
readonly EXIT_SYMLINK_FAILED=4
readonly EXIT_USER_ABORT=5

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Global variables
CLAUDE_DIR="$HOME/.claude"
REPO_AGENTS_DIR="$SCRIPT_DIR/agents"
REPO_COMMANDS_DIR="$SCRIPT_DIR/commands"
AGENTS_PATH_TYPE=""
COMMANDS_PATH_TYPE=""
BACKUP_DIR=""

# Error handling function
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit "${2:-1}"
}

# Success message function
success_msg() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Warning message function
warning_msg() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Info message function
info_msg() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Log function with timestamp
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Validate repository directory structure
validate_repository() {
    log "Validating repository directory structure"
    
    if [[ ! -d "$REPO_AGENTS_DIR" ]]; then
        error_exit "agents/ directory not found at: $REPO_AGENTS_DIR" $EXIT_INVALID_REPO
    fi
    
    if [[ ! -d "$REPO_COMMANDS_DIR" ]]; then
        error_exit "commands/ directory not found at: $REPO_COMMANDS_DIR" $EXIT_INVALID_REPO
    fi
    
    # Verify agents directory has content
    if [[ -z "$(ls -A "$REPO_AGENTS_DIR" 2>/dev/null)" ]]; then
        warning_msg "agents/ directory is empty at: $REPO_AGENTS_DIR"
    fi
    
    # Verify commands directory has content
    if [[ -z "$(ls -A "$REPO_COMMANDS_DIR" 2>/dev/null)" ]]; then
        warning_msg "commands/ directory is empty at: $REPO_COMMANDS_DIR"
    fi
    
    success_msg "Repository directory structure validated"
}

# Validate script execution location
validate_execution_location() {
    log "Validating script execution location"
    
    local current_dir="$(pwd)"
    
    if [[ "$current_dir" != "$SCRIPT_DIR" ]]; then
        error_exit "Script must be run from repository root. Current: $current_dir, Expected: $SCRIPT_DIR" $EXIT_INVALID_LOCATION
    fi
    
    # Additional check - ensure we're in a directory that contains the expected structure
    if [[ ! -f "$SCRIPT_DIR/$SCRIPT_NAME" ]]; then
        error_exit "Script not found in current directory: $SCRIPT_DIR/$SCRIPT_NAME" $EXIT_INVALID_LOCATION
    fi
    
    success_msg "Script execution location validated: $SCRIPT_DIR"
}

# Print colored header
print_header() {
    echo -e "${BLUE}=====================================${NC}"
    echo -e "${BLUE}  Claude Code Configuration Installer${NC}"
    echo -e "${BLUE}=====================================${NC}"
    echo
}

# Print separator line
print_separator() {
    echo -e "${BLUE}-------------------------------------${NC}"
}

# Ask user for confirmation
ask_confirmation() {
    local message="$1"
    local response
    
    echo -n -e "${YELLOW}$message [y/N]: ${NC}"
    read -r response
    
    case "$response" in
        [yY][eE][sS]|[yY]) return 0 ;;
        *) return 1 ;;
    esac
}

# Display absolute path in a consistent format
display_path() {
    local path="$1"
    echo -e "${BLUE}$path${NC}"
}

# Verbose progress indicator
progress_msg() {
    echo -e "${GREEN}▶ $1${NC}"
}

# Analyze existing path (directory, symlink, file, or non-existent)
analyze_path() {
    local path="$1"
    local path_type=""
    
    if [[ -L "$path" ]]; then
        path_type="symlink"
    elif [[ -d "$path" ]]; then
        path_type="directory"
    elif [[ -f "$path" ]]; then
        path_type="file"
    else
        path_type="none"
    fi
    
    echo "$path_type"
}

# Analyze existing ~/.claude paths
analyze_claude_paths() {
    log "Analyzing existing ~/.claude paths"
    
    local agents_path="$CLAUDE_DIR/agents"
    local commands_path="$CLAUDE_DIR/commands"
    
    # Analyze agents path
    local agents_type=$(analyze_path "$agents_path")
    info_msg "~/.claude/agents: $agents_type"
    
    case "$agents_type" in
        "symlink")
            local target=$(readlink "$agents_path")
            info_msg "  → Links to: $(display_path "$target")"
            if [[ ! -e "$target" ]]; then
                warning_msg "  → Symlink target does not exist!"
            fi
            ;;
        "directory")
            local count=$(find "$agents_path" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
            info_msg "  → Contains $count files"
            ;;
        "file")
            warning_msg "  → Unexpected file at agents location"
            ;;
        "none")
            info_msg "  → Does not exist"
            ;;
    esac
    
    # Analyze commands path
    local commands_type=$(analyze_path "$commands_path")
    info_msg "~/.claude/commands: $commands_type"
    
    case "$commands_type" in
        "symlink")
            local target=$(readlink "$commands_path")
            info_msg "  → Links to: $(display_path "$target")"
            if [[ ! -e "$target" ]]; then
                warning_msg "  → Symlink target does not exist!"
            fi
            ;;
        "directory")
            local count=$(find "$commands_path" -maxdepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')
            info_msg "  → Contains $count files"
            ;;
        "file")
            warning_msg "  → Unexpected file at commands location"
            ;;
        "none")
            info_msg "  → Does not exist"
            ;;
    esac
    
    # Store results in global variables for other functions
    AGENTS_PATH_TYPE="$agents_type"
    COMMANDS_PATH_TYPE="$commands_type"
    
    success_msg "Path analysis completed"
}

# Create backup directory name with timestamp
create_backup_dir_name() {
    local base_dir="$HOME/.claude-backup"
    local backup_name="claude-backup-$TIMESTAMP"
    local backup_path="$base_dir/$backup_name"
    
    echo "$backup_path"
}

# Prepare backup directory structure
prepare_backup_directory() {
    log "Preparing backup directory structure"
    
    BACKUP_DIR=$(create_backup_dir_name)
    local base_backup_dir="$HOME/.claude-backup"
    
    # Create base backup directory if it doesn't exist
    if [[ ! -d "$base_backup_dir" ]]; then
        progress_msg "Creating backup directory: $(display_path "$base_backup_dir")"
        mkdir -p "$base_backup_dir" || error_exit "Failed to create backup directory: $base_backup_dir" $EXIT_BACKUP_FAILED
    fi
    
    # Create timestamped backup directory
    progress_msg "Creating timestamped backup: $(display_path "$BACKUP_DIR")"
    mkdir -p "$BACKUP_DIR" || error_exit "Failed to create timestamped backup directory: $BACKUP_DIR" $EXIT_BACKUP_FAILED
    
    success_msg "Backup directory prepared: $(display_path "$BACKUP_DIR")"
}

# Backup existing directory
backup_directory() {
    local source_path="$1"
    local backup_name="$2"
    local backup_path="$BACKUP_DIR/$backup_name"
    
    if [[ ! -d "$source_path" ]]; then
        info_msg "Skipping backup of $source_path (not a directory)"
        return 0
    fi
    
    progress_msg "Backing up directory: $(display_path "$source_path")"
    
    # Use cp -r to preserve permissions and structure
    cp -r "$source_path" "$backup_path" || {
        error_exit "Failed to backup directory from $source_path to $backup_path" $EXIT_BACKUP_FAILED
    }
    
    success_msg "Directory backed up to: $(display_path "$backup_path")"
}

# Create backups for existing directories
create_backups() {
    log "Creating backups for existing directories"
    
    local needs_backup=false
    
    # Check if agents directory needs backup
    if [[ "$AGENTS_PATH_TYPE" == "directory" ]]; then
        backup_directory "$CLAUDE_DIR/agents" "agents"
        needs_backup=true
    fi
    
    # Check if commands directory needs backup
    if [[ "$COMMANDS_PATH_TYPE" == "directory" ]]; then
        backup_directory "$CLAUDE_DIR/commands" "commands"
        needs_backup=true
    fi
    
    if [[ "$needs_backup" == "false" ]]; then
        info_msg "No directories require backup"
    else
        success_msg "All necessary backups completed in: $(display_path "$BACKUP_DIR")"
    fi
}

# Remove existing symlinks (no backup needed)
remove_symlinks() {
    log "Removing existing symlinks"
    
    local removed_any=false
    
    # Remove agents symlink if it exists
    if [[ "$AGENTS_PATH_TYPE" == "symlink" ]]; then
        progress_msg "Removing existing agents symlink: $(display_path "$CLAUDE_DIR/agents")"
        rm "$CLAUDE_DIR/agents" || error_exit "Failed to remove agents symlink" $EXIT_BACKUP_FAILED
        success_msg "Agents symlink removed"
        removed_any=true
    fi
    
    # Remove commands symlink if it exists
    if [[ "$COMMANDS_PATH_TYPE" == "symlink" ]]; then
        progress_msg "Removing existing commands symlink: $(display_path "$CLAUDE_DIR/commands")"
        rm "$CLAUDE_DIR/commands" || error_exit "Failed to remove commands symlink" $EXIT_BACKUP_FAILED
        success_msg "Commands symlink removed"
        removed_any=true
    fi
    
    if [[ "$removed_any" == "false" ]]; then
        info_msg "No symlinks to remove"
    fi
}

# Perform complete backup and cleanup process
perform_backup_process() {
    log "Starting backup process"
    
    # First analyze what exists
    analyze_claude_paths
    
    # Check if we need to do any backup work
    local needs_work=false
    if [[ "$AGENTS_PATH_TYPE" == "directory" ]] || [[ "$AGENTS_PATH_TYPE" == "symlink" ]]; then
        needs_work=true
    fi
    if [[ "$COMMANDS_PATH_TYPE" == "directory" ]] || [[ "$COMMANDS_PATH_TYPE" == "symlink" ]]; then
        needs_work=true
    fi
    
    if [[ "$needs_work" == "false" ]]; then
        info_msg "No existing agents or commands directories/symlinks found - skipping backup process"
        return 0
    fi
    
    # Prepare backup directory structure
    prepare_backup_directory
    
    # Create backups for existing directories (this validates backup can be created)
    create_backups
    
    # Remove existing symlinks (no backup needed)
    remove_symlinks
    
    # Handle any remaining files that are not directories or symlinks
    if [[ "$AGENTS_PATH_TYPE" == "file" ]]; then
        warning_msg "Found file at ~/.claude/agents - backing up as 'agents-file'"
        cp "$CLAUDE_DIR/agents" "$BACKUP_DIR/agents-file" || error_exit "Failed to backup agents file" $EXIT_BACKUP_FAILED
        rm "$CLAUDE_DIR/agents" || error_exit "Failed to remove agents file" $EXIT_BACKUP_FAILED
        success_msg "Agents file backed up and removed"
    fi
    
    if [[ "$COMMANDS_PATH_TYPE" == "file" ]]; then
        warning_msg "Found file at ~/.claude/commands - backing up as 'commands-file'"
        cp "$CLAUDE_DIR/commands" "$BACKUP_DIR/commands-file" || error_exit "Failed to backup commands file" $EXIT_BACKUP_FAILED
        rm "$CLAUDE_DIR/commands" || error_exit "Failed to remove commands file" $EXIT_BACKUP_FAILED
        success_msg "Commands file backed up and removed"
    fi
    
    success_msg "Backup process completed successfully"
}

# Ensure ~/.claude directory exists
ensure_claude_directory() {
    log "Ensuring ~/.claude directory exists"
    
    if [[ ! -d "$CLAUDE_DIR" ]]; then
        progress_msg "Creating ~/.claude directory: $(display_path "$CLAUDE_DIR")"
        mkdir -p "$CLAUDE_DIR" || error_exit "Failed to create ~/.claude directory: $CLAUDE_DIR" $EXIT_SYMLINK_FAILED
        success_msg "~/.claude directory created"
    else
        info_msg "~/.claude directory already exists"
    fi
    
    # Verify directory is writable
    if [[ ! -w "$CLAUDE_DIR" ]]; then
        error_exit "~/.claude directory is not writable: $CLAUDE_DIR" $EXIT_SYMLINK_FAILED
    fi
    
    success_msg "~/.claude directory ready: $(display_path "$CLAUDE_DIR")"
}

# Create symlink from ~/.claude/agents to repo/agents
create_agents_symlink() {
    log "Creating agents symlink"
    
    local target_path="$REPO_AGENTS_DIR"
    local link_path="$CLAUDE_DIR/agents"
    
    # Verify target directory exists
    if [[ ! -d "$target_path" ]]; then
        error_exit "Target agents directory does not exist: $target_path" $EXIT_SYMLINK_FAILED
    fi
    
    # Ensure link path is clear (should be after backup process)
    if [[ -e "$link_path" ]]; then
        error_exit "Something still exists at link path: $link_path" $EXIT_SYMLINK_FAILED
    fi
    
    # Create the symlink
    progress_msg "Creating symlink: $(display_path "$link_path") → $(display_path "$target_path")"
    ln -sf "$target_path" "$link_path" || error_exit "Failed to create agents symlink" $EXIT_SYMLINK_FAILED
    
    # Verify symlink was created correctly
    if [[ ! -L "$link_path" ]]; then
        error_exit "Symlink was not created: $link_path" $EXIT_SYMLINK_FAILED
    fi
    
    # Verify symlink points to correct target
    local actual_target=$(readlink "$link_path")
    if [[ "$actual_target" != "$target_path" ]]; then
        error_exit "Symlink points to wrong target. Expected: $target_path, Actual: $actual_target" $EXIT_SYMLINK_FAILED
    fi
    
    success_msg "Agents symlink created successfully"
}

# Create symlink from ~/.claude/commands to repo/commands
create_commands_symlink() {
    log "Creating commands symlink"
    
    local target_path="$REPO_COMMANDS_DIR"
    local link_path="$CLAUDE_DIR/commands"
    
    # Verify target directory exists
    if [[ ! -d "$target_path" ]]; then
        error_exit "Target commands directory does not exist: $target_path" $EXIT_SYMLINK_FAILED
    fi
    
    # Ensure link path is clear (should be after backup process)
    if [[ -e "$link_path" ]]; then
        error_exit "Something still exists at link path: $link_path" $EXIT_SYMLINK_FAILED
    fi
    
    # Create the symlink
    progress_msg "Creating symlink: $(display_path "$link_path") → $(display_path "$target_path")"
    ln -sf "$target_path" "$link_path" || error_exit "Failed to create commands symlink" $EXIT_SYMLINK_FAILED
    
    # Verify symlink was created correctly
    if [[ ! -L "$link_path" ]]; then
        error_exit "Symlink was not created: $link_path" $EXIT_SYMLINK_FAILED
    fi
    
    # Verify symlink points to correct target
    local actual_target=$(readlink "$link_path")
    if [[ "$actual_target" != "$target_path" ]]; then
        error_exit "Symlink points to wrong target. Expected: $target_path, Actual: $actual_target" $EXIT_SYMLINK_FAILED
    fi
    
    success_msg "Commands symlink created successfully"
}

# Validate created symlinks
validate_symlinks() {
    log "Validating created symlinks"
    
    local agents_link="$CLAUDE_DIR/agents"
    local commands_link="$CLAUDE_DIR/commands"
    local validation_failed=false
    
    # Validate agents symlink
    info_msg "Validating agents symlink..."
    if [[ ! -L "$agents_link" ]]; then
        error_exit "Agents symlink does not exist: $agents_link" $EXIT_SYMLINK_FAILED
    fi
    
    local agents_target=$(readlink "$agents_link")
    if [[ "$agents_target" != "$REPO_AGENTS_DIR" ]]; then
        error_exit "Agents symlink has wrong target. Expected: $REPO_AGENTS_DIR, Found: $agents_target" $EXIT_SYMLINK_FAILED
    fi
    
    if [[ ! -d "$agents_target" ]]; then
        error_exit "Agents symlink target does not exist: $agents_target" $EXIT_SYMLINK_FAILED
    fi
    
    # Count files in agents directory
    local agents_count=$(find "$agents_target" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    info_msg "  → Agents directory accessible with $agents_count .md files"
    
    # Validate commands symlink
    info_msg "Validating commands symlink..."
    if [[ ! -L "$commands_link" ]]; then
        error_exit "Commands symlink does not exist: $commands_link" $EXIT_SYMLINK_FAILED
    fi
    
    local commands_target=$(readlink "$commands_link")
    if [[ "$commands_target" != "$REPO_COMMANDS_DIR" ]]; then
        error_exit "Commands symlink has wrong target. Expected: $REPO_COMMANDS_DIR, Found: $commands_target" $EXIT_SYMLINK_FAILED
    fi
    
    if [[ ! -d "$commands_target" ]]; then
        error_exit "Commands symlink target does not exist: $commands_target" $EXIT_SYMLINK_FAILED
    fi
    
    # Count files in commands directory
    local commands_count=$(find "$commands_target" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    info_msg "  → Commands directory accessible with $commands_count .md files"
    
    success_msg "All symlinks validated successfully"
}

# Perform complete symlink creation process
create_symlinks() {
    log "Starting symlink creation process"
    
    # Step 1: Ensure ~/.claude directory exists
    ensure_claude_directory
    
    # Step 2: Create agents symlink
    progress_msg "Step 1/2: Creating agents symlink"
    create_agents_symlink
    
    # Step 3: Create commands symlink
    progress_msg "Step 2/2: Creating commands symlink"
    create_commands_symlink
    
    # Step 4: Validate all symlinks
    validate_symlinks
    
    success_msg "Symlink creation process completed successfully"
}

# Analyze current state and present installation plan
analyze_and_confirm() {
    log "Analyzing current configuration and creating installation plan"
    
    print_separator
    info_msg "PRE-INSTALLATION ANALYSIS"
    print_separator
    
    # Analyze current state
    analyze_claude_paths
    
    # Present installation plan
    echo
    info_msg "INSTALLATION PLAN"
    print_separator
    
    echo -e "${BLUE}The following changes will be made:${NC}"
    echo
    
    # Show what will happen to existing items
    if [[ "$AGENTS_PATH_TYPE" == "directory" ]]; then
        echo -e "• ${YELLOW}BACKUP${NC}: Existing ~/.claude/agents directory → $(display_path "$HOME/.claude-backup/claude-backup-$TIMESTAMP/agents")"
    elif [[ "$AGENTS_PATH_TYPE" == "symlink" ]]; then
        local current_target=$(readlink "$CLAUDE_DIR/agents" 2>/dev/null || echo "unknown")
        echo -e "• ${YELLOW}REPLACE${NC}: Existing ~/.claude/agents symlink (→ $current_target)"
    elif [[ "$AGENTS_PATH_TYPE" == "file" ]]; then
        echo -e "• ${YELLOW}BACKUP${NC}: Existing ~/.claude/agents file → $(display_path "$HOME/.claude-backup/claude-backup-$TIMESTAMP/agents-file")"
    fi
    
    if [[ "$COMMANDS_PATH_TYPE" == "directory" ]]; then
        echo -e "• ${YELLOW}BACKUP${NC}: Existing ~/.claude/commands directory → $(display_path "$HOME/.claude-backup/claude-backup-$TIMESTAMP/commands")"
    elif [[ "$COMMANDS_PATH_TYPE" == "symlink" ]]; then
        local current_target=$(readlink "$CLAUDE_DIR/commands" 2>/dev/null || echo "unknown")
        echo -e "• ${YELLOW}REPLACE${NC}: Existing ~/.claude/commands symlink (→ $current_target)"
    elif [[ "$COMMANDS_PATH_TYPE" == "file" ]]; then
        echo -e "• ${YELLOW}BACKUP${NC}: Existing ~/.claude/commands file → $(display_path "$HOME/.claude-backup/claude-backup-$TIMESTAMP/commands-file")"
    fi
    
    # Show what will be created
    echo
    echo -e "• ${GREEN}CREATE${NC}: ~/.claude/agents → $(display_path "$REPO_AGENTS_DIR")"
    echo -e "• ${GREEN}CREATE${NC}: ~/.claude/commands → $(display_path "$REPO_COMMANDS_DIR")"
    
    # Show repository contents summary
    echo
    info_msg "REPOSITORY CONTENTS"
    print_separator
    
    local agents_count=$(find "$REPO_AGENTS_DIR" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    local commands_count=$(find "$REPO_COMMANDS_DIR" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    
    echo -e "• ${BLUE}Agents${NC}: $agents_count custom agent definitions"
    echo -e "• ${BLUE}Commands${NC}: $commands_count custom slash commands"
    
    # Show backup location if needed
    local needs_backup=false
    if [[ "$AGENTS_PATH_TYPE" == "directory" ]] || [[ "$AGENTS_PATH_TYPE" == "file" ]]; then
        needs_backup=true
    fi
    if [[ "$COMMANDS_PATH_TYPE" == "directory" ]] || [[ "$COMMANDS_PATH_TYPE" == "file" ]]; then
        needs_backup=true
    fi
    
    if [[ "$needs_backup" == "true" ]]; then
        echo
        warning_msg "Backups will be stored in: $(display_path "$HOME/.claude-backup/claude-backup-$TIMESTAMP")"
    fi
    
    echo
    print_separator
    
    # Ask for confirmation
    if ! ask_confirmation "Proceed with installation?"; then
        info_msg "Installation cancelled by user"
        exit $EXIT_USER_ABORT
    fi
    
    success_msg "Installation confirmed - proceeding..."
}

# Display final installation summary
display_final_summary() {
    log "Displaying final installation summary"
    
    print_separator
    success_msg "INSTALLATION COMPLETED SUCCESSFULLY!"
    print_separator
    
    echo -e "${GREEN}✓${NC} Claude Code configuration has been installed"
    echo
    
    info_msg "INSTALLED COMPONENTS"
    print_separator
    
    # Show created symlinks
    if [[ -L "$CLAUDE_DIR/agents" ]]; then
        local agents_target=$(readlink "$CLAUDE_DIR/agents")
        local agents_count=$(find "$agents_target" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        echo -e "• ${GREEN}Agents${NC}: $(display_path "$CLAUDE_DIR/agents") → $(display_path "$agents_target")"
        echo -e "  └─ $agents_count custom agent definitions available"
    fi
    
    if [[ -L "$CLAUDE_DIR/commands" ]]; then
        local commands_target=$(readlink "$CLAUDE_DIR/commands")
        local commands_count=$(find "$commands_target" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        echo -e "• ${GREEN}Commands${NC}: $(display_path "$CLAUDE_DIR/commands") → $(display_path "$commands_target")"
        echo -e "  └─ $commands_count custom slash commands available"
    fi
    
    # Show backup information if any backups were created
    if [[ -n "$BACKUP_DIR" ]] && [[ -d "$BACKUP_DIR" ]]; then
        echo
        info_msg "BACKUP INFORMATION"
        print_separator
        echo -e "• ${YELLOW}Backups stored in${NC}: $(display_path "$BACKUP_DIR")"
        
        # List what was backed up
        local backup_items=()
        [[ -d "$BACKUP_DIR/agents" ]] && backup_items+=("agents directory")
        [[ -d "$BACKUP_DIR/commands" ]] && backup_items+=("commands directory")
        [[ -f "$BACKUP_DIR/agents-file" ]] && backup_items+=("agents file")
        [[ -f "$BACKUP_DIR/commands-file" ]] && backup_items+=("commands file")
        
        if [[ ${#backup_items[@]} -gt 0 ]]; then
            for item in "${backup_items[@]}"; do
                echo -e "  └─ Backed up: $item"
            done
        fi
    fi
    
    echo
    info_msg "NEXT STEPS"
    print_separator
    
    echo -e "1. ${BLUE}Restart Claude Code${NC} or reload your configuration to use the new agents and commands"
    echo -e "2. ${BLUE}Test the installation${NC} by trying custom commands like:"
    echo -e "   └─ Type ${YELLOW}/build:${NC} to see available build commands"
    echo -e "   └─ Use ${YELLOW}@quality-reviewer${NC} to invoke the quality review agent"
    echo -e "3. ${BLUE}Explore the repository${NC} to understand available agents and commands:"
    echo -e "   └─ Agents: $(display_path "$REPO_AGENTS_DIR")"
    echo -e "   └─ Commands: $(display_path "$REPO_COMMANDS_DIR")"
    
    if [[ -f "$SCRIPT_DIR/README.md" ]]; then
        echo -e "4. ${BLUE}Read the documentation${NC}: $(display_path "$SCRIPT_DIR/README.md")"
    fi
    
    echo
    success_msg "Installation complete! Your Claude Code configuration is now active."
}

# Main function
main() {
    print_header
    log "Starting Claude Code configuration installer"
    
    # Phase 1: Foundation validation
    validate_execution_location
    validate_repository
    
    # Phase 2: Pre-installation analysis and user confirmation
    analyze_and_confirm
    
    # Phase 3: Backup existing configuration
    print_separator
    perform_backup_process
    
    # Phase 4: Create symlinks
    print_separator
    create_symlinks
    
    # Phase 5: Final summary
    print_separator
    display_final_summary
    
    exit $EXIT_SUCCESS
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi