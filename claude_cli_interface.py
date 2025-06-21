#!/usr/bin/env python3
"""
A CLI interface for claude-code-sdk that mimics the Claude Code CLI experience.
"""

import asyncio
import sys
import os
from claude_code_sdk import query, ClaudeCodeOptions
from ui_theme import Colors, Icons, Theme


async def main():
    print(Theme.header("Claude CLI Interface", 60))
    print(f"{Colors.MUTED}Type 'exit' or 'quit' to end the conversation{Colors.RESET}")
    print()
    
    options = ClaudeCodeOptions(
        permission_mode='default',  # Can be changed to 'acceptEdits' or 'bypassPermissions'
        cwd='.',
        continue_conversation=True
    )
    
    while True:
        try:
            # Get user input
            prompt = input(f"\n{Theme.prompt('You', options.permission_mode)}").strip()
            
            if prompt.lower() in ['exit', 'quit']:
                print(Theme.status("Goodbye!", 'success'))
                break
            
            if not prompt:
                continue
            
            print(f"\n{Colors.PRIMARY}Claude{Colors.RESET}: ", end="", flush=True)
            
            # Query Claude
            response_parts = []
            async for message in query(prompt=prompt, options=options):
                if hasattr(message, 'content'):
                    # Handle AssistantMessage
                    for block in message.content:
                        if hasattr(block, 'text'):
                            response_parts.append(block.text)
                            print(block.text, end="", flush=True)
                        elif hasattr(block, 'name'):
                            # Tool use block
                            params = block.input if hasattr(block, 'input') else {}
                            print(Theme.tool_use(block.name, params), end="", flush=True)
                elif hasattr(message, 'result'):
                    # Handle ResultMessage
                    if message.total_cost_usd:
                        print(f"\n\n{Colors.MUTED}[Cost: ${message.total_cost_usd:.4f}]{Colors.RESET}", end="")
            
            print()  # New line after response
            
        except KeyboardInterrupt:
            print(f"\n\n{Theme.status('Interrupted. Type \'exit\' to quit.', 'warning')}")
        except Exception as e:
            print(f"\n{Theme.status(f'Error: {e}', 'error')}")


if __name__ == "__main__":
    asyncio.run(main())