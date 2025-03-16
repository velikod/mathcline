# Math Repository

This repository contains mathematical tools and scripts using Python libraries including NumPy, Pandas, scikit-learn, and Manim for mathematical animations.

## Setup Instructions

### Prerequisites

- Miniconda or Anaconda (recommended for managing Python environments and dependencies)

### Setting Up the Environment

1. **Install Miniconda** (if not already installed):
   ```bash
   # Download Miniconda installer
   curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh

   # Install Miniconda
   bash Miniconda3-latest-MacOSX-arm64.sh -b

   # Initialize conda for your shell
   ~/miniconda3/bin/conda init zsh  # or bash, depending on your shell

   # Restart your terminal or source your shell config
   source ~/.zshrc  # or ~/.bashrc
   ```

2. **Create the conda environment**:
   ```bash
   # Create environment from environment.yml
   conda env create -f environment.yml
   ```

   Alternatively, you can run the setup script:
   ```bash
   chmod +x setup_conda_env.sh
   ./setup_conda_env.sh
   ```

3. **Activate the environment**:
   ```bash
   conda activate mathenv
   ```

4. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Testing the Installation

1. **Test basic imports**:
   ```bash
   python -c "import numpy; import pandas; import sklearn; import matplotlib; import sympy; print('Basic packages working!')"
   ```

2. **Test Manim**:
   ```bash
   python test_manim.py
   ```

3. **Render a Manim animation**:
   ```bash
   manim -pql test_manim.py SquareToCircle
   ```

## Environment Details

The Python environment includes:
- Python 3.10
- NumPy, Pandas, scikit-learn for data analysis
- Matplotlib and Sympy for visualization and symbolic mathematics
- Manim 0.19.0 for creating mathematical animations
- Supporting libraries (Cairo, Pango, FFmpeg) for rendering

## Development Workflow

### Pre-commit Hooks

This repository uses pre-commit hooks to maintain code quality. The hooks include:

- Code formatting with Black
- Import sorting with isort
- Linting with flake8 (with relaxed docstring requirements)
- Basic file checks (trailing whitespace, file endings, etc.)

The pre-commit hooks run automatically when you commit changes. To run them manually:

```bash
pre-commit run --all-files
```

## License

[Add license information]
