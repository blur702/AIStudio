#!/usr/bin/env python3
"""
Automated builder that monitors GitHub for specification updates
and builds projects automatically using claude-code-sdk
"""

import asyncio
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
from claude_code_sdk import query, ClaudeCodeOptions


class GitHubAutomatedBuilder:
    def __init__(self, config_file="builder_config.json"):
        with open(config_file) as f:
            self.config = json.load(f)
        
        self.specs_repo = self.config["specs_repo"]
        self.output_repo = self.config["output_repo"]
        self.work_dir = Path(self.config["work_directory"])
        self.specs_dir = self.work_dir / "specs"
        self.output_dir = self.work_dir / "output"
        
        # Ensure API key is available
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    def git_pull(self, repo_path):
        """Pull latest changes from git repo"""
        subprocess.run(["git", "pull"], cwd=repo_path, check=True)
    
    def git_push(self, repo_path, message):
        """Commit and push changes"""
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
    
    def clone_if_needed(self, repo_url, target_path):
        """Clone repository if it doesn't exist"""
        if not target_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", repo_url, str(target_path)], check=True)
    
    async def build_project_from_specs(self):
        """Build project based on specifications"""
        options = ClaudeCodeOptions(
            permission_mode='bypassPermissions',
            cwd=str(self.output_dir),
            max_turns=100,
            system_prompt="""You are an expert software engineer building production applications.
            Follow all specifications exactly. Implement comprehensive error handling and testing.
            Create professional, maintainable code following best practices."""
        )
        
        # Load all specification files
        specs_content = []
        for spec_file in self.specs_dir.glob("**/*.md"):
            content = spec_file.read_text()
            specs_content.append(f"=== {spec_file.name} ===\n{content}")
        
        for spec_file in self.specs_dir.glob("**/*.json"):
            with open(spec_file) as f:
                content = json.dumps(json.load(f), indent=2)
                specs_content.append(f"=== {spec_file.name} ===\n{content}")
        
        # Build the project
        build_prompt = f"""
        Build a complete project based on these specifications:
        
        {chr(10).join(specs_content)}
        
        Requirements:
        1. Create all necessary files and directories
        2. Implement all specified features
        3. Add comprehensive error handling
        4. Include unit tests with >80% coverage
        5. Add integration tests for key workflows
        6. Create documentation (README.md, API docs)
        7. Include CI/CD configuration files
        8. Add docker support if applicable
        9. Ensure the code is production-ready
        """
        
        total_cost = 0.0
        print(f"\n[{datetime.now()}] Starting automated build...")
        
        async for message in query(prompt=build_prompt, options=options):
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'name') and hasattr(block, 'input'):
                        # Log tool usage
                        tool_name = block.name
                        if tool_name in ['Write', 'Edit']:
                            file_path = block.input.get('file_path', 'unknown')
                            print(f"  📝 {tool_name}: {file_path}")
                        elif tool_name == 'Bash':
                            command = block.input.get('command', 'unknown')
                            print(f"  💻 Running: {command[:50]}...")
            elif hasattr(message, 'total_cost_usd'):
                total_cost = message.total_cost_usd
        
        print(f"✅ Build complete! Total cost: ${total_cost:.4f}")
        return total_cost
    
    async def run_continuous_build(self):
        """Continuously monitor and build when specs change"""
        print(f"🤖 GitHub Automated Builder Started")
        print(f"   Specs repo: {self.specs_repo}")
        print(f"   Output repo: {self.output_repo}")
        print(f"   Check interval: {self.config.get('check_interval_minutes', 30)} minutes")
        
        # Initial setup
        self.clone_if_needed(self.specs_repo, self.specs_dir)
        self.clone_if_needed(self.output_repo, self.output_dir)
        
        last_build_hash = None
        
        while True:
            try:
                # Pull latest specs
                print(f"\n[{datetime.now()}] Checking for updates...")
                self.git_pull(self.specs_dir)
                
                # Check if specs have changed
                current_hash = subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], 
                    cwd=self.specs_dir
                ).decode().strip()
                
                if current_hash != last_build_hash:
                    print(f"📋 New specifications detected: {current_hash[:8]}")
                    
                    # Build the project
                    cost = await self.build_project_from_specs()
                    
                    # Commit and push results
                    self.git_push(
                        self.output_dir,
                        f"Automated build from specs {current_hash[:8]} (Cost: ${cost:.4f})"
                    )
                    
                    last_build_hash = current_hash
                    
                    # Log build
                    with open(self.work_dir / "build_log.json", "a") as f:
                        json.dump({
                            "timestamp": datetime.now().isoformat(),
                            "specs_hash": current_hash,
                            "cost": cost,
                            "status": "success"
                        }, f)
                        f.write("\n")
                else:
                    print("  No changes detected")
                
                # Wait before next check
                await asyncio.sleep(self.config.get('check_interval_minutes', 30) * 60)
                
            except Exception as e:
                print(f"❌ Error during build: {e}")
                # Log error
                with open(self.work_dir / "build_log.json", "a") as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "error": str(e),
                        "status": "failed"
                    }, f)
                    f.write("\n")
                
                # Wait before retry
                await asyncio.sleep(300)  # 5 minutes


async def main():
    # Create example config if it doesn't exist
    config_path = Path("builder_config.json")
    if not config_path.exists():
        example_config = {
            "specs_repo": "https://github.com/yourusername/project-specs.git",
            "output_repo": "https://github.com/yourusername/generated-project.git",
            "work_directory": "/opt/code/automated_builds",
            "check_interval_minutes": 30
        }
        config_path.write_text(json.dumps(example_config, indent=2))
        print("Created example config at builder_config.json")
        print("Please update it with your repository URLs and run again.")
        return
    
    builder = GitHubAutomatedBuilder()
    await builder.run_continuous_build()


if __name__ == "__main__":
    asyncio.run(main())