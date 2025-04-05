#!/bin/bash
# This script will set up the conda environment for the math repository

# Make sure conda is initialized
source ~/miniconda3/etc/profile.d/conda.sh

# Remove any existing mathenv environment
conda env remove -n mathenv -y

# Create environment from the environment.yml file
conda env create -f environment.yml

# Activate the environment
conda activate mathenv

# Test the installation
echo "Testing installation..."
python -c "import numpy; import matplotlib; import sympy; print('Basic packages working!')"
python -c "import sphinx; import sphinx_rtd_theme; print('Documentation packages working!')"

echo ""
echo "Setup complete!"
echo "To activate this environment, run: conda activate mathenv"
