#!/usr/bin/env python3
"""
Automated project builder using claude-code-sdk
Reads project specs and builds entire applications automatically
"""

import asyncio
import json
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions


class ProjectAutomator:
    def __init__(self, project_dir, specs_dir):
        self.project_dir = Path(project_dir)
        self.specs_dir = Path(specs_dir)
        self.options = ClaudeCodeOptions(
            permission_mode='bypassPermissions',  # Auto-accept all operations
            cwd=str(self.project_dir),
            max_turns=50,  # Allow longer conversations
            system_prompt="""You are an expert software engineer building production-ready applications.
            Follow specifications exactly and implement best practices."""
        )
        
    async def load_specifications(self):
        """Load all project specification documents"""
        specs = {}
        for spec_file in self.specs_dir.glob("*.md"):
            specs[spec_file.stem] = spec_file.read_text()
        
        for spec_file in self.specs_dir.glob("*.json"):
            with open(spec_file) as f:
                specs[spec_file.stem] = json.load(f)
        
        return specs
    
    async def build_component(self, component_name, spec_content):
        """Build a single component based on specifications"""
        prompt = f"""
        Build the {component_name} component based on these specifications:
        
        {spec_content}
        
        Create all necessary files, implement the functionality, add tests, and ensure production quality.
        Use appropriate error handling and follow the project's coding standards.
        """
        
        print(f"\n🔨 Building component: {component_name}")
        
        async for message in query(prompt=prompt, options=self.options):
            # Log progress
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'name'):
                        print(f"   • Executing: {block.name}")
            elif hasattr(message, 'result'):
                print(f"   ✅ Component built (Cost: ${message.total_cost_usd:.4f})")
    
    async def build_project(self):
        """Build entire project from specifications"""
        print(f"🚀 Starting automated project build")
        print(f"   Project directory: {self.project_dir}")
        print(f"   Specifications: {self.specs_dir}")
        
        # Create project directory if needed
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # Load all specifications
        specs = await self.load_specifications()
        print(f"\n📋 Found {len(specs)} specification documents")
        
        # Build initial project structure
        structure_prompt = f"""
        Initialize a new project with the following specifications:
        {json.dumps(list(specs.keys()), indent=2)}
        
        Create the appropriate directory structure, package.json/requirements.txt,
        configuration files, and initial boilerplate.
        """
        
        print("\n🏗️  Setting up project structure...")
        async for message in query(prompt=structure_prompt, options=self.options):
            pass
        
        # Build each component
        for component, spec in specs.items():
            await self.build_component(component, spec)
        
        # Final integration and testing
        print("\n🧪 Running final integration and tests...")
        test_prompt = """
        Now that all components are built:
        1. Ensure all components work together
        2. Run linting and fix any issues
        3. Run all tests and fix any failures
        4. Create a README.md with usage instructions
        """
        
        async for message in query(prompt=test_prompt, options=self.options):
            pass
        
        print("\n✨ Project build complete!")


async def main():
    # Example usage
    automator = ProjectAutomator(
        project_dir="/opt/code/my_automated_project",
        specs_dir="/opt/code/project_specs"
    )
    
    await automator.build_project()


if __name__ == "__main__":
    asyncio.run(main())