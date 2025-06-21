#!/usr/bin/env python3
"""
Test script to demonstrate the UI improvements without actually calling Claude API
"""

from ui_theme import Colors, Icons, Theme
import time

def test_ui_components():
    print("\n" + "="*80)
    print("UI THEME DEMONSTRATION")
    print("="*80 + "\n")
    
    # Test header
    print("1. Headers:")
    print(Theme.header("Claude CLI Interface", 60))
    print()
    
    # Test status messages
    print("2. Status Messages:")
    print(Theme.status("Operation completed successfully", 'success'))
    print(Theme.status("Warning: Permission mode is elevated", 'warning'))
    print(Theme.status("Error: File not found", 'error'))
    print(Theme.status("Info: Connected to Claude API", 'info'))
    print()
    
    # Test prompts
    print("3. Prompts (different permission modes):")
    print("Default mode: " + Theme.prompt("~/projects", "default"))
    print("Accept edits: " + Theme.prompt("~/projects", "acceptEdits"))
    print("Bypass perms: " + Theme.prompt("~/projects", "bypassPermissions"))
    print()
    
    # Test tool usage
    print("4. Tool Usage Display:")
    print(Theme.tool_use("Edit", {"file_path": "/path/to/file.py"}))
    print(Theme.tool_use("Bash", {"command": "npm install"}))
    print(Theme.tool_use("Read", {"file_path": "README.md"}))
    print()
    
    # Test box
    print("5. Box Component:")
    content = "Session Duration: 45.2s\nMessages Exchanged: 12\nTools Used: 5"
    print(Theme.box(content, "Session Status", Colors.INFO))
    print()
    
    # Test help section
    print("6. Help Section:")
    commands = [
        ('/help', 'Show this help message'),
        ('/model [name]', 'Set or show the model'),
        ('/clear', 'Clear the screen'),
    ]
    print(Theme.help_section("Available Commands", commands))
    print()
    
    # Test progress bar
    print("7. Progress Bar:")
    for i in range(0, 101, 10):
        print(f"\rProgress: {Theme.progress_bar(i, 100, 40)}", end="", flush=True)
        time.sleep(0.1)
    print("\n")
    
    # Test session summary
    print("8. Session Summary:")
    print(Theme.session_summary(
        duration_ms=45200,
        turns=6,
        cost=0.0234,
        tools_used=["Edit", "Bash", "Read", "Edit", "Write"]
    ))
    print()
    
    # Color palette showcase
    print("9. Color Palette:")
    print(f"{Colors.PRIMARY}Primary Color{Colors.RESET}")
    print(f"{Colors.SECONDARY}Secondary Color{Colors.RESET}")
    print(f"{Colors.SUCCESS}Success Color{Colors.RESET}")
    print(f"{Colors.WARNING}Warning Color{Colors.RESET}")
    print(f"{Colors.ERROR}Error Color{Colors.RESET}")
    print(f"{Colors.INFO}Info Color{Colors.RESET}")
    print(f"{Colors.MUTED}Muted Color{Colors.RESET}")
    print(f"{Colors.ACCENT}Accent Color{Colors.RESET}")
    print()
    
    # Icons showcase
    print("10. Icons:")
    print(f"Success: {Icons.SUCCESS}  Error: {Icons.ERROR}  Warning: {Icons.WARNING}  Info: {Icons.INFO}")
    print(f"Tools: {Icons.TOOL}  Edit: {Icons.FILE_EDIT}  Write: {Icons.FILE_WRITE}  Read: {Icons.FILE_READ}")
    print(f"Terminal: {Icons.TERMINAL}  Search: {Icons.SEARCH}  Prompt: {Icons.PROMPT}  Arrow: {Icons.ARROW_RIGHT}")
    print()

if __name__ == "__main__":
    test_ui_components()