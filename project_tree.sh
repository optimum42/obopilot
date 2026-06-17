#!/bin/bash

# ============================================================
# Project Structure Preview
# ------------------------------------------------------------
# Displays the project directory tree including hidden files
# while excluding temporary, cache and IDE-specific folders.
# ============================================================

# ------------------------------------------------------------
# Check if tree is installed
# ------------------------------------------------------------

if ! command -v tree &> /dev/null
then
    echo "'tree' is not installed."

    # --------------------------------------------------------
    # Check if Homebrew is installed
    # --------------------------------------------------------

    if ! command -v brew &> /dev/null
    then
        echo "'Homebrew' is not installed."
        echo "Installing Homebrew..."

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    echo "Installing tree via Homebrew..."

    brew install tree
fi

# ------------------------------------------------------------
# Display project structure
# ------------------------------------------------------------

tree -a -L 3 \
-I ".DS_Store|__pycache__|*.pyc|.pytest_cache|.venv|.env|*.egg-info|.git|.idea"