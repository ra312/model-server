#!/bin/bash

# Set the virtual environment name
venv_name="my_jupyter_kernel"

# Create the virtual environment
python3 -m venv $venv_name

# Activate the virtual environment
source $venv_name/bin/activate

# Install Jupyter Notebook
pip install jupyter

# Install the ipykernel package
pip install ipykernel

# Register the virtual environment with Jupyter
python -m ipykernel install --user --name=$venv_name --display-name=$venv_name

# Deactivate the virtual environment
deactivate
