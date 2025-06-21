#!/usr/bin/env python3
"""
Modern UI theme and styling utilities for the Claude CLI interfaces.
Uses ANSI escape codes for rich terminal output.
"""

import sys
import os
from typing import Optional, Dict, Any
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    # Base colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Modern color palette - inspired by GitHub Dark theme
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright variants
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Custom theme colors
    PRIMARY = '\033[38;2;88;166;255m'      # Bright blue
    SECONDARY = '\033[38;2;139;148;158m'   # Muted gray
    SUCCESS = '\033[38;2;87;171;90m'       # Green
    WARNING = '\033[38;2;242;157;65m'      # Orange
    ERROR = '\033[38;2;249;117;131m'       # Red
    INFO = '\033[38;2;64;156;255m'         # Blue
    MUTED = '\033[38;2;110;119;129m'       # Dark gray
    ACCENT = '\033[38;2;201;209;217m'      # Light gray


class Icons:
    """Modern unicode icons for better visual representation"""
    # Status icons
    SUCCESS = '✓'
    ERROR = '✗'
    WARNING = '⚠'
    INFO = 'ℹ'
    
    # Action icons
    PROMPT = '❯'
    ARROW_RIGHT = '→'
    ARROW_LEFT = '←'
    BULLET = '•'
    
    # Tool icons
    TOOL = '⚡'
    FILE_EDIT = '✎'
    FILE_WRITE = '📄'
    FILE_READ = '👁'
    TERMINAL = '⌨'
    SEARCH = '🔍'
    
    # UI elements
    BOX_TOP_LEFT = '╭'
    BOX_TOP_RIGHT = '╮'
    BOX_BOTTOM_LEFT = '╰'
    BOX_BOTTOM_RIGHT = '╯'
    BOX_HORIZONTAL = '─'
    BOX_VERTICAL = '│'
    BOX_CROSS = '┼'
    
    # Progress
    SPINNER = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    PROGRESS_EMPTY = '░'
    PROGRESS_FULL = '█'


class Theme:
    """UI theme utilities for consistent styling"""
    
    @staticmethod
    def header(text: str, width: int = 80) -> str:
        """Create a styled header"""
        padding = (width - len(text) - 2) // 2
        line = f"{Colors.MUTED}{Icons.BOX_HORIZONTAL * width}{Colors.RESET}"
        header = f"{Colors.PRIMARY}{Colors.BOLD}{' ' * padding}{text}{' ' * (width - padding - len(text) - 2)}{Colors.RESET}"
        return f"{line}\n{header}\n{line}"
    
    @staticmethod
    def box(content: str, title: Optional[str] = None, color: str = Colors.SECONDARY) -> str:
        """Create a box around content"""
        lines = content.split('\n')
        max_width = max(len(line) for line in lines)
        if title:
            max_width = max(max_width, len(title) + 2)
        
        result = []
        
        # Top border
        if title:
            title_str = f" {title} "
            padding = (max_width - len(title)) // 2
            top = f"{color}{Icons.BOX_TOP_LEFT}{Icons.BOX_HORIZONTAL * padding}{Colors.BOLD}{title_str}{Colors.RESET}{color}{Icons.BOX_HORIZONTAL * (max_width - padding - len(title_str) + 2)}{Icons.BOX_TOP_RIGHT}{Colors.RESET}"
        else:
            top = f"{color}{Icons.BOX_TOP_LEFT}{Icons.BOX_HORIZONTAL * (max_width + 2)}{Icons.BOX_TOP_RIGHT}{Colors.RESET}"
        result.append(top)
        
        # Content
        for line in lines:
            padding = max_width - len(line)
            result.append(f"{color}{Icons.BOX_VERTICAL}{Colors.RESET} {line}{' ' * padding} {color}{Icons.BOX_VERTICAL}{Colors.RESET}")
        
        # Bottom border
        bottom = f"{color}{Icons.BOX_BOTTOM_LEFT}{Icons.BOX_HORIZONTAL * (max_width + 2)}{Icons.BOX_BOTTOM_RIGHT}{Colors.RESET}"
        result.append(bottom)
        
        return '\n'.join(result)
    
    @staticmethod
    def prompt(cwd: str, mode: str = 'default') -> str:
        """Create a styled prompt"""
        time = datetime.now().strftime('%H:%M')
        mode_indicator = {
            'default': f"{Colors.INFO}◆{Colors.RESET}",
            'acceptEdits': f"{Colors.WARNING}◈{Colors.RESET}",
            'bypassPermissions': f"{Colors.ERROR}◉{Colors.RESET}"
        }.get(mode, '')
        
        return f"{Colors.MUTED}[{time}]{Colors.RESET} {mode_indicator} {Colors.PRIMARY}{cwd}{Colors.RESET} {Colors.ACCENT}{Icons.PROMPT}{Colors.RESET} "
    
    @staticmethod
    def status(message: str, status: str = 'info') -> str:
        """Create a status message with icon"""
        icons_colors = {
            'success': (Icons.SUCCESS, Colors.SUCCESS),
            'error': (Icons.ERROR, Colors.ERROR),
            'warning': (Icons.WARNING, Colors.WARNING),
            'info': (Icons.INFO, Colors.INFO),
        }
        icon, color = icons_colors.get(status, (Icons.INFO, Colors.INFO))
        return f"{color}{icon}{Colors.RESET} {message}"
    
    @staticmethod
    def tool_use(tool_name: str, params: Dict[str, Any]) -> str:
        """Format tool usage display"""
        tool_icons = {
            'Edit': Icons.FILE_EDIT,
            'Write': Icons.FILE_WRITE,
            'Read': Icons.FILE_READ,
            'Bash': Icons.TERMINAL,
            'Search': Icons.SEARCH,
        }
        icon = tool_icons.get(tool_name, Icons.TOOL)
        
        result = f"\n{Colors.SECONDARY}{'─' * 60}{Colors.RESET}\n"
        result += f"{Colors.WARNING}{icon} {Colors.BOLD}{tool_name}{Colors.RESET}"
        
        # Add relevant parameters
        if tool_name in ['Edit', 'Write', 'Read'] and 'file_path' in params:
            result += f" {Colors.MUTED}{Icons.ARROW_RIGHT}{Colors.RESET} {Colors.ACCENT}{params['file_path']}{Colors.RESET}"
        elif tool_name == 'Bash' and 'command' in params:
            cmd = params['command']
            if len(cmd) > 50:
                cmd = cmd[:47] + '...'
            result += f" {Colors.MUTED}{Icons.ARROW_RIGHT}{Colors.RESET} {Colors.ACCENT}{cmd}{Colors.RESET}"
        
        result += f"\n{Colors.SECONDARY}{'─' * 60}{Colors.RESET}"
        return result
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 30) -> str:
        """Create a progress bar"""
        if total == 0:
            return ""
        
        percentage = current / total
        filled = int(width * percentage)
        empty = width - filled
        
        bar = f"{Colors.SUCCESS}{Icons.PROGRESS_FULL * filled}{Colors.MUTED}{Icons.PROGRESS_EMPTY * empty}{Colors.RESET}"
        return f"[{bar}] {percentage*100:.1f}%"
    
    @staticmethod
    def session_summary(duration_ms: int, turns: int, cost: Optional[float], tools_used: list) -> str:
        """Format session summary"""
        duration_s = duration_ms / 1000
        
        summary_lines = [
            f"{Colors.SECONDARY}{'═' * 60}{Colors.RESET}",
            f"{Colors.PRIMARY}{Colors.BOLD}Session Summary{Colors.RESET}",
            f"{Colors.SECONDARY}{'─' * 60}{Colors.RESET}",
            f"{Icons.BULLET} Duration: {Colors.ACCENT}{duration_s:.2f}s{Colors.RESET}",
            f"{Icons.BULLET} Turns: {Colors.ACCENT}{turns}{Colors.RESET}",
        ]
        
        if cost:
            summary_lines.append(f"{Icons.BULLET} Cost: {Colors.SUCCESS}${cost:.4f}{Colors.RESET}")
        
        if tools_used:
            unique_tools = list(set(tools_used))
            summary_lines.append(f"{Icons.BULLET} Tools: {Colors.INFO}{', '.join(unique_tools)}{Colors.RESET}")
        
        summary_lines.append(f"{Colors.SECONDARY}{'═' * 60}{Colors.RESET}")
        
        return '\n'.join(summary_lines)
    
    @staticmethod
    def help_section(title: str, items: list) -> str:
        """Format a help section"""
        result = [f"\n{Colors.PRIMARY}{Colors.BOLD}{title}{Colors.RESET}"]
        for item in items:
            if isinstance(item, tuple):
                cmd, desc = item
                result.append(f"  {Colors.ACCENT}{cmd:<25}{Colors.RESET} {Colors.MUTED}{desc}{Colors.RESET}")
            else:
                result.append(f"  {Colors.MUTED}{item}{Colors.RESET}")
        return '\n'.join(result)


def supports_color() -> bool:
    """Check if the terminal supports color"""
    # Disable color for pipes and files
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return False
    
    # Check for color support indicators
    if os.getenv('COLORTERM') in ('truecolor', '24bit'):
        return True
    if os.getenv('TERM') in ('xterm-256color', 'screen-256color', 'tmux-256color'):
        return True
    
    return True


# Disable colors if not supported
if not supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_'):
            setattr(Colors, attr, '')