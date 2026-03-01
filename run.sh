#!/bin/bash

# run.sh - Script to run the liulianmao-fastapi application

set -e

echo "Starting liulianmao-fastapi application..."

# Get the current directory
CURRENT_DIR="$(pwd)"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found. Please run this script from the project root directory."
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies if needed
echo "Installing dependencies with Poetry..."
poetry install --no-root

# Run the application
echo "Starting FastAPI server..."
echo "Server will be available at: http://localhost:9000"
echo "Press Ctrl+C to stop the server"

# Run with uvicorn - using src.main as the module path
# We need to set PYTHONPATH to include the src directory
PYTHONPATH="${CURRENT_DIR}/src:$PYTHONPATH" poetry run uvicorn src.main:app --host 0.0.0.0 --port 9000 --reload