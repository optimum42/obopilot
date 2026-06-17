#!/bin/bash

# ------------------------------------------------------------
# Template safety check
# ------------------------------------------------------------

CURRENT_DIR=$(basename "$PWD")

echo ""
echo "===================================================="
echo " TEMPLATE SETUP CHECK"
echo "===================================================="
echo ""
echo "Current project directory:"
echo "  $CURRENT_DIR"
echo ""

if [ "$CURRENT_DIR" = "PROJECT_TEMPLATE" ]; then

    echo "ERROR:"
    echo "The project directory is still named:"
    echo ""
    echo "  PROJECT_TEMPLATE"
    echo ""
    echo "Please rename the project directory before"
    echo "running setup.sh."
    echo ""
    echo "Example:"
    echo ""
    echo "  PROJECT_TEMPLATE"
    echo "          ↓"
    echo "  movie-database-project"
    echo ""

    exit 1
fi

echo "Have you already renamed the project directory?"
echo ""
read -p "Type 'yes' to continue: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo ""
    echo "Setup aborted."
    exit 1
fi

echo ""
echo "Project directory confirmed."
echo ""


set -e

echo "==================================="
echo "Setting up project..."
echo "==================================="

# ------------------------------------------------------------
# Detect project/package name
# ------------------------------------------------------------

PROJECT_NAME=$(basename "$PWD")
PACKAGE_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr '-' '_')

echo ""
echo "Project name detected: $PROJECT_NAME"
echo "Package name: $PACKAGE_NAME"

# ------------------------------------------------------------
# Create src directory and package
# ------------------------------------------------------------

mkdir -p src

if [ -d "src/myproject" ] && [ "$PACKAGE_NAME" != "myproject" ]; then
    echo ""
    echo "Renaming src/myproject to src/$PACKAGE_NAME ..."
    mv src/myproject "src/$PACKAGE_NAME"
fi

if [ ! -d "src/$PACKAGE_NAME" ]; then
    echo ""
    echo "Creating src/$PACKAGE_NAME package ..."
    mkdir -p "src/$PACKAGE_NAME"
    touch "src/$PACKAGE_NAME/__init__.py"
    touch "src/$PACKAGE_NAME/main.py"
fi

# ------------------------------------------------------------
# Create pyproject.toml
# ------------------------------------------------------------

if [ ! -f pyproject.toml ]; then

cat > pyproject.toml <<EOF
[project]
name = "$PACKAGE_NAME"
version = "0.1.0"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["src"]
EOF

echo ""
echo "Created pyproject.toml"

else
    echo ""
    echo "pyproject.toml already exists"
fi

# ------------------------------------------------------------
# Create requirements.txt
# ------------------------------------------------------------

if [ ! -f requirements.txt ]; then

cat > requirements.txt <<EOF
requests
python-dotenv
pytest
SQLAlchemy
EOF

echo ""
echo "Created requirements.txt"

else
    echo ""
    echo "requirements.txt already exists"
fi

# ------------------------------------------------------------
# Create virtual environment
# ------------------------------------------------------------

echo ""
echo "Creating virtual environment..."

python3 -m venv .venv

# ------------------------------------------------------------
# Upgrade pip
# ------------------------------------------------------------

echo ""
echo "Upgrading pip..."

.venv/bin/pip install --upgrade pip

# ------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------

echo ""
echo "Installing dependencies..."

.venv/bin/pip install -r requirements.txt

# ------------------------------------------------------------
# Install project in editable mode
# ------------------------------------------------------------

echo ""
echo "Installing project in editable mode..."

.venv/bin/pip install -e .

# ------------------------------------------------------------
# Finished
# ------------------------------------------------------------

echo ""
echo "==================================="
echo "Setup completed successfully."
echo "==================================="

echo ""
echo "Activate the virtual environment with:"
echo "source .venv/bin/activate"