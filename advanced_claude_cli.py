#!/usr/bin/env python3
"""
Advanced CLI interface with features similar to the real Claude Code CLI.
Supports commands, options, and rich output formatting.
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions, ResultMessage, AssistantMessage, SystemMessage
from ui_theme import Colors, Icons, Theme


class ClaudeCliInterface:
    def __init__(self):
        self.session_id = None
        self.options = ClaudeCodeOptions(
            permission_mode='default',
            cwd=os.getcwd()
        )
        
    def parse_command(self, input_str):
        """Parse special commands like /help, /model, etc."""
        if input_str.startswith('/'):
            parts = input_str.split(maxsplit=1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""
            
            if command == '/help':
                self.show_help()
                return None
            elif command == '/model':
                if args:
                    self.options.model = args
                    print(Theme.status(f"Model set to: {args}", 'success'))
                else:
                    print(Theme.status(f"Current model: {self.options.model or 'default'}", 'info'))
                return None
            elif command == '/cwd':
                if args:
                    path = Path(args).expanduser().resolve()
                    if path.exists() and path.is_dir():
                        self.options.cwd = str(path)
                        print(Theme.status(f"Working directory set to: {path}", 'success'))
                    else:
                        print(Theme.status(f"Invalid directory: {args}", 'error'))
                else:
                    print(Theme.status(f"Current working directory: {self.options.cwd}", 'info'))
                return None
            elif command == '/permission':
                if args in ['default', 'acceptEdits', 'bypassPermissions']:
                    self.options.permission_mode = args
                    print(Theme.status(f"Permission mode set to: {args}", 'success'))
                else:
                    print(Theme.status(f"Current permission mode: {self.options.permission_mode}", 'info'))
                    print(f"{Colors.MUTED}Valid modes: default, acceptEdits, bypassPermissions{Colors.RESET}")
                return None
            elif command == '/clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                return None
            else:
                print(Theme.status(f"Unknown command: {command}", 'error'))
                print(f"{Colors.MUTED}Type /help for available commands{Colors.RESET}")
                return None
        
        return input_str
    
    def show_help(self):
        """Display help information."""
        commands = [
            ('/help', 'Show this help message'),
            ('/model [name]', 'Set or show the model'),
            ('/cwd [path]', 'Set or show working directory'),
            ('/permission [mode]', 'Set permission mode'),
            ('/clear', 'Clear the screen'),
            ('exit, quit', 'Exit the interface'),
        ]
        
        examples = [
            'What files are in this directory?',
            '/model claude-3-opus-20240229',
            '/cwd ~/projects',
            'Create a Python hello world script',
        ]
        
        print(Theme.header("Claude CLI Help", 60))
        print(Theme.help_section("Commands", commands))
        print(Theme.help_section("Examples", examples))
        print(f"\n{Colors.MUTED}Permission modes: default, acceptEdits, bypassPermissions{Colors.RESET}")
    
    async def run_conversation(self, prompt):
        """Run a single conversation turn with Claude."""
        try:
            message_count = 0
            tool_uses = []
            
            async for message in query(prompt=prompt, options=self.options):
                message_count += 1
                
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            print(block.text, end="", flush=True)
                        elif hasattr(block, 'name'):
                            tool_uses.append(block.name)
                            print(Theme.tool_use(block.name, block.input if hasattr(block, 'input') else {}))
                
                elif isinstance(message, SystemMessage):
                    if message.subtype == 'tool_result':
                        # Could show tool results if desired
                        pass
                
                elif isinstance(message, ResultMessage):
                    print("\n" + Theme.session_summary(
                        message.duration_ms,
                        message.num_turns,
                        message.total_cost_usd,
                        tool_uses
                    ))
                    self.session_id = message.session_id
            
            print()  # Final newline
            
        except Exception as e:
            print(f"\n{Theme.status(f'Error: {e}', 'error')}")
    
    async def run(self):
        """Main CLI loop."""
        print(Theme.header("Claude CLI Interface", 60))
        print(f"{Colors.MUTED}Type /help for commands, or 'exit' to quit{Colors.RESET}")
        print()
        
        while True:
            try:
                # Show prompt with working directory
                cwd = Path(self.options.cwd).name
                prompt_str = input(f"\n{Theme.prompt(cwd, self.options.permission_mode)}").strip()
                
                if prompt_str.lower() in ['exit', 'quit']:
                    print(Theme.status("Goodbye!", 'success'))
                    break
                
                if not prompt_str:
                    continue
                
                # Parse for commands
                parsed = self.parse_command(prompt_str)
                if parsed is None:
                    continue
                
                # Run the conversation
                await self.run_conversation(parsed)
                
            except KeyboardInterrupt:
                print(f"\n\n{Theme.status('Interrupted. Type \'exit\' to quit.', 'warning')}")
            except EOFError:
                print(f"\n{Theme.status('Goodbye!', 'success')}")
                break


async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Claude CLI Interface')
    parser.add_argument('prompt', nargs='*', help='Initial prompt')
    parser.add_argument('--model', help='Model to use')
    parser.add_argument('--permission', choices=['default', 'acceptEdits', 'bypassPermissions'],
                       help='Permission mode')
    parser.add_argument('--cwd', help='Working directory')
    
    args = parser.parse_args()
    
    cli = ClaudeCliInterface()
    
    # Apply command line options
    if args.model:
        cli.options.model = args.model
    if args.permission:
        cli.options.permission_mode = args.permission
    if args.cwd:
        cli.options.cwd = args.cwd
    
    # If prompt provided via command line, run it and exit
    if args.prompt:
        prompt = ' '.join(args.prompt)
        await cli.run_conversation(prompt)
    else:
        # Interactive mode
        await cli.run()


if __name__ == "__main__":
    asyncio.run(main())