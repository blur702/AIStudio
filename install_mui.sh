#!/bin/bash
set -e

echo "Installing Material-UI (MUI) dependencies..."

cd /opt/claude-react/claude-ui

# Install MUI core components and icons
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material @mui/lab @mui/x-data-grid

echo "✓ MUI dependencies installed successfully!"
echo ""
echo "Installed packages:"
echo "- @mui/material - Core MUI components"
echo "- @emotion/react - CSS-in-JS library (MUI dependency)"
echo "- @emotion/styled - Styled components for MUI"
echo "- @mui/icons-material - Material Design icons"
echo "- @mui/lab - Lab components (experimental)"
echo "- @mui/x-data-grid - Advanced data grid component"