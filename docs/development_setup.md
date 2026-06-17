# Project Template Workflow

This project is designed as a reusable GitHub template for future Python projects.

After creating a new repository from the template, follow this recommended setup workflow.

---

# 1. Clone the Repository

```bash
git clone <new-repository-url>
cd <new-project-folder>
```

---

# 2. Rename the Python Package

Rename the default package folder:

```bash
mv src/myproject src/movieapp
```

Replace `movieapp` with your actual project/package name.

---

# 3. Update Python Imports

Update all imports in the project files.

Example:

Before:

```python
from myproject.config import CONFIG
```

After:

```python
from movieapp.config import CONFIG
```

---

# 4. Update `pyproject.toml`

Adjust the project metadata:

```toml
[project]
name = "movieapp"
version = "0.1.0"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["src"]
```

The package finder automatically detects the renamed package inside `src/`.

---

# 5. Run the Setup Script

Execute the setup script:

```bash
./setup.sh
```

The script will:

- create the virtual environment
- upgrade pip
- install dependencies
- install the project in editable mode

---

# 6. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

---

# 7. Run Tests

```bash
pytest
```

This verifies that:

- imports work correctly
- the package was installed successfully
- the project setup is valid

---

# 8. Update the README

Customize:

- project title
- description
- screenshots
- features
- usage examples

---

# 9. Create the Initial Commit

```bash
git add .
git commit -m "initial project setup"
```

---

# Important Notes

The command:

```bash
pip install -e .
```

should always be executed **after** renaming the package folder and updating `pyproject.toml`.

Otherwise the old package name may still be installed inside the virtual environment.

---

# Recommended Naming Conventions

## Repository Name

Use readable GitHub repository names:

```text
movie-database-project
```

---

## Python Package Name

Use short lowercase import-friendly package names:

```text
movieapp
```

Avoid:

- spaces
- uppercase letters
- hyphens

because Python imports do not support them.

---

# Detaild explanation for Development Setup

---

## Editable Installation (`pip install -e .`)

This project uses the recommended modern Python `src/` layout.

To make the package importable during development and testing, install the project in editable mode.

---

## Command

```bash
pip install -e .
```

---

## What it does

The `-e` flag means:

```text
editable mode
```

Instead of copying the package into Python's `site-packages` directory, Python creates a link to the local project folder.

This means:

- code changes become immediately available
- no reinstallation is required after edits
- imports work correctly across the entire project
- tests can import the package cleanly

---

## Why this is important

With the `src/` layout:

```text
project/
├── src/
│   └── myproject/
```

Python cannot automatically find the package unless it is installed.

After running:

```bash
pip install -e .
```

imports work correctly:

```python
from myproject.main import main
```

---

## Recommended Development Workflow

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

#### macOS / Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

### 3. Install project in editable mode

```bash
pip install -e .
```

---

### 4. Install development dependencies (optional)

```bash
pip install pytest
```

or later via:

```bash
pip install -e ".[dev]"
```

---

## Typical Usage

Run application:

```bash
python src/myproject/main.py
```

Run tests:

```bash
pytest
```

---

## Key Takeaway

```text
pip install -e .
```

links the Python environment directly to the local project source code and is the standard approach for professional Python development projects.