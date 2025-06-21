#!/usr/bin/env python3
"""
A modern CLI interface for claude-code-sdk with enhanced UI.
Features clean design, better visual feedback, and improved user experience.
"""

import asyncio
import sys
import os
from datetime import datetime
from claude_code_sdk import query, ClaudeCodeOptions, ResultMessage, AssistantMessage, SystemMessage
from ui_theme import Colors, Icons, Theme


class ModernClaudeInterface:
    def __init__(self):
        self.session_id = None
        self.options = ClaudeCodeOptions(
            permission_mode='default',
            cwd=os.getcwd(),
            continue_conversation=True
        )
        self.message_count = 0
        self.start_time = None
        
    def show_welcome(self):
        """Display welcome message with modern styling"""
        print(Theme.header("Claude AI Assistant", 60))
        print(f"{Colors.MUTED}Powered by claude-code-sdk")
        print(f"Type 'exit' or 'quit' to end • '/help' for commands{Colors.RESET}\n")
        
    def show_help(self):
        """Display help with modern formatting"""
        commands = [
            ('exit, quit', 'End the conversation'),
            ('/help', 'Show this help message'),
            ('/clear', 'Clear the screen'),
            ('/status', 'Show session status'),
        ]
        
        tips = [
            'Ask me to help with coding tasks',
            'I can read, write, and edit files',
            'I can run terminal commands',
            'I track costs and provide session summaries',
        ]
        
        print(Theme.help_section("Commands", commands))
        print(Theme.help_section("Tips", tips))
    
    def show_status(self):
        """Display current session status"""
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            status_text = f"Session Duration: {duration:.1f}s | Messages: {self.message_count}"
        else:
            status_text = "No active session"
        
        print(Theme.box(status_text, "Session Status", Colors.INFO))
    
    def format_assistant_response(self, text: str) -> str:
        """Apply subtle formatting to assistant responses"""
        # Could add markdown parsing here for even richer output
        return text
    
    async def run_conversation(self, prompt: str):
        """Run a single conversation turn with enhanced UI"""
        if not self.start_time:
            self.start_time = datetime.now()
        
        self.message_count += 1
        tool_uses = []
        response_started = False
        
        try:
            # Show thinking indicator
            print(f"\n{Colors.PRIMARY}Claude{Colors.RESET} {Colors.MUTED}is thinking...{Colors.RESET}", end='\r')
            
            async for message in query(prompt=prompt, options=self.options):
                if isinstance(message, AssistantMessage):
                    if not response_started:
                        # Clear thinking indicator and show response header
                        print(f"\r{' ' * 50}\r", end='')  # Clear line
                        print(f"{Colors.PRIMARY}Claude{Colors.RESET}:", end=" ")
                        response_started = True
                    
                    for block in message.content:
                        if hasattr(block, 'text'):
                            formatted_text = self.format_assistant_response(block.text)
                            print(formatted_text, end="", flush=True)
                        elif hasattr(block, 'name'):
                            tool_uses.append(block.name)
                            # Show tool usage with theme
                            params = block.input if hasattr(block, 'input') else {}
                            print(Theme.tool_use(block.name, params))
                            response_started = True
                
                elif isinstance(message, SystemMessage):
                    if message.subtype == 'tool_result' and hasattr(message, 'content'):
                        # Optionally show tool results in a subtle way
                        if message.content and len(str(message.content)) < 100:
                            print(f"\n{Colors.MUTED}→ {message.content}{Colors.RESET}")
                
                elif isinstance(message, ResultMessage):
                    # Store session info
                    self.session_id = message.session_id
                    
                    # Show mini summary inline (not the full box)
                    if message.total_cost_usd:
                        cost_str = f" {Colors.MUTED}[${message.total_cost_usd:.4f}]{Colors.RESET}"
                    else:
                        cost_str = ""
                    
                    if tool_uses:
                        tools_str = f" {Colors.MUTED}[{len(set(tool_uses))} tools]{Colors.RESET}"
                    else:
                        tools_str = ""
                    
                    print(f"{cost_str}{tools_str}")
            
            if not response_started:
                # Clear thinking indicator if no response
                print(f"\r{' ' * 50}\r", end='')
            
        except Exception as e:
            print(f"\r{' ' * 50}\r", end='')  # Clear any pending output
            print(Theme.status(f"Error: {e}", 'error'))
    
    async def run(self):
        """Main interaction loop with modern UI"""
        self.show_welcome()
        
        while True:
            try:
                # Modern prompt with time and mode indicator
                prompt_str = input(f"\n{Theme.prompt('You', self.options.permission_mode)}").strip()
                
                if prompt_str.lower() in ['exit', 'quit']:
                    # Show session summary if we had interactions
                    if self.start_time and self.message_count > 0:
                        duration_ms = int((datetime.now() - self.start_time).total_seconds() * 1000)
                        print("\n" + Theme.session_summary(duration_ms, self.message_count, None, []))
                    print(Theme.status("Thank you for using Claude. Goodbye!", 'success'))
                    break
                
                if not prompt_str:
                    continue
                
                # Handle commands
                if prompt_str == '/help':
                    self.show_help()
                    continue
                elif prompt_str == '/clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    self.show_welcome()
                    continue
                elif prompt_str == '/status':
                    self.show_status()
                    continue
                
                # Run the conversation
                await self.run_conversation(prompt_str)
                
            except KeyboardInterrupt:
                print(f"\n\n{Theme.status('Interrupted. Type exit to quit or continue chatting.', 'warning')}")
            except EOFError:
                print(f"\n{Theme.status('Thank you for using Claude. Goodbye!', 'success')}")
                break


async def main():
    """Main entry point"""
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Usage: python claude_cli_interface.py")
        print("An interactive CLI for Claude AI with modern UI")
        return
    
    interface = ModernClaudeInterface()
    await interface.run()


if __name__ == "__main__":
    asyncio.run(main())