#!/bin/bash
# Script to rebuild claude-react frontend with corrected API endpoints

echo "Fixing claude-react frontend build..."
echo "This script will rebuild the frontend with the correct /api/code endpoints"
echo ""

# First, let's verify the changes are in place
echo "1. Checking source files for correct endpoints..."
if grep -q "/api/code" /opt/claude-react/claude-ui/src/components/ClaudeInterface.tsx; then
    echo "✓ ClaudeInterface.tsx has correct /api/code endpoints"
else
    echo "✗ ClaudeInterface.tsx still has old endpoints"
    exit 1
fi

if grep -q "base: '/code/'" /opt/claude-react/claude-ui/vite.config.ts; then
    echo "✓ vite.config.ts has correct base path"
else
    echo "✗ vite.config.ts still has old base path"
    exit 1
fi

echo ""
echo "2. Source files are correct. The issue is that the frontend hasn't been rebuilt."
echo ""
echo "To fix this, run the following commands:"
echo ""
echo "cd /opt/claude-react/claude-ui"
echo "npm run build"
echo ""
echo "Note: You may see TypeScript errors during build. You can either:"
echo "1. Fix the TypeScript errors first, or"
echo "2. Temporarily disable TypeScript checking in the build"
echo ""
echo "After rebuilding, the site at https://kevinalthaus.com/code/ should show 'Ready' status."