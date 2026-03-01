#!/bin/bash

# run.sh - Unified script to run the liulianmao-fastapi application
# Usage: ./run.sh [--simple|-simple]

set -e

# Default mode
MODE="poetry"

# Parse command line arguments
for arg in "$@"; do
    case $arg in
        --simple|-simple)
            MODE="simple"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTION]"
            echo "Run the liulianmao-fastapi application"
            echo ""
            echo "Options:"
            echo "  --simple, -simple    Run without Poetry (simple mode)"
            echo "  --help, -h           Show this help message"
            echo ""
            echo "Default mode: Use Poetry for dependency management"
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "Starting liulianmao-fastapi application..."
echo "Mode: $MODE"

# Get the current directory
CURRENT_DIR="$(pwd)"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found. Please run this script from the project root directory."
    exit 1
fi

if [ "$MODE" = "poetry" ]; then
    # Poetry mode
    echo "Using Poetry for dependency management..."
    
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
else
    # Simple mode (without Poetry)
    echo "Using simple mode (without Poetry)..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo "Error: python3 is not installed."
        exit 1
    fi
    
    # Check if uvicorn is installed
    if ! python3 -c "import uvicorn" 2>/dev/null; then
        echo "uvicorn is not installed. Installing dependencies..."
        
        # Try to install using poetry if available
        if command -v poetry &> /dev/null; then
            echo "Using Poetry to install dependencies..."
            poetry install --no-root
        else
            echo "Warning: Poetry not found, trying to install from pyproject.toml..."
            # Try to parse and install dependencies from pyproject.toml
            if grep -q "dependencies" pyproject.toml; then
                echo "Installing dependencies from pyproject.toml..."
                # Extract dependencies and install them
                pip install fastapi "uvicorn[standard]" loguru pillow liulianmao
            else
                echo "Error: Cannot determine dependencies to install."
                echo "Please install Poetry first or manually install required packages:"
                echo "  pip install fastapi uvicorn loguru pillow liulianmao"
                exit 1
            fi
        fi
    fi
    
    # Run the application
    echo "Starting FastAPI server..."
    echo "Server will be available at: http://localhost:9000"
    echo "Press Ctrl+C to stop the server"
    
    # Run with uvicorn
    cd src && python3 -m uvicorn main:app --host 0.0.0.0 --port 9000 --reload
fi