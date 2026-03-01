#!/bin/bash

# run-simple.sh - Simple script to run the liulianmao-fastapi application without Poetry

set -e

echo "Starting liulianmao-fastapi application (simple version)..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found. Please run this script from the project root directory."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Check if uvicorn is installed
if ! python3 -c "import uvicorn" 2>/dev/null; then
    echo "uvicorn is not installed. Installing dependencies..."
    pip install -r <(poetry export --without-hashes --format=requirements.txt)
fi

# Run the application
echo "Starting FastAPI server..."
echo "Server will be available at: http://localhost:9000"
echo "Press Ctrl+C to stop the server"

# Run with uvicorn
cd src && python3 -m uvicorn main:app --host 0.0.0.0 --port 9000 --reload