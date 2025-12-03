#!/bin/bash

# This script helps set up .env files for the codexa-core project
# You need to manually create .env files with your API keys and configuration
#
# Required .env files:
#   - .env (root directory)
#   - app/server/.env (if using the server)
#
# See docs/API_KEYS_REFERENCE.md for required environment variables

echo "Checking for .env files..."

# Check root .env file
if [ -f ".env" ]; then
    echo "✓ Root .env file exists"
else
    echo "✗ Root .env file is missing"
    echo "  Create .env in the root directory with your environment variables"
    echo "  See docs/API_KEYS_REFERENCE.md for details"
fi

# Check server .env file
if [ -f "app/server/.env" ]; then
    echo "✓ Server .env file exists"
else
    echo "✗ Server .env file is missing"
    echo "  Create app/server/.env with your server configuration"
    echo "  See docs/API_KEYS_REFERENCE.md for details"
fi

echo ""
echo "NOTE: This script previously referenced '../tac-5/' which no longer exists."
echo "You must manually create .env files with your own configuration."