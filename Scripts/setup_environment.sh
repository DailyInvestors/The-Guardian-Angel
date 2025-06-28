#!/bin/bash

# This script creates a Python virtual environment and installs all required dependencies.
# It is designed to be run from the root directory of the GuardianAI project.

# --- Configuration ---
VENV_DIR="venv"
PYTHON_CMD="python3"

# --- Style and Messaging ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting GuardianAI Environment Setup...${NC}"

# 1. Check for Python 3
if ! command -v $PYTHON_CMD &> /dev/null
then
    echo "Error: ${PYTHON_CMD} is not installed or not in PATH. Please install Python 3.8+."
    exit 1
fi

echo "✅ Python 3 found."

# 2. Create the Python Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in './${VENV_DIR}'..."
    $PYTHON_CMD -m venv $VENV_DIR
else
    echo "Virtual environment './${VENV_DIR}' already exists."
fi

# 3. Activate the Virtual Environment
# The 'source' command must be used to run this in the current shell context.
source $VENV_DIR/bin/activate
echo "✅ Virtual environment activated."

# 4. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null

# 5. Install Dependencies
# We install from requirements-dev.txt, which includes requirements.txt.
# This ensures developers get all tools needed for contribution.
echo "Installing all required packages from requirements-dev.txt..."
if pip install -r requirements-dev.txt; then
    echo "✅ Dependencies installed successfully."
else
    echo "Error: Failed to install dependencies. Please check the error messages above."
    exit 1
fi

# --- Final Instructions ---
echo -e "\n${GREEN}🎉 Setup Complete! 🎉${NC}"
echo "The virtual environment '${VENV_DIR}' is now active."
echo "You can now run and develop GuardianAI."
echo "To deactivate this environment later, simply run: ${YELLOW}deactivate${NC}"