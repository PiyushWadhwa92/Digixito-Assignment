# PowerShell setup script for the assignment project

# Create virtual environment
python -m venv .venv

# Activate the virtual environment
& .venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
python -m pip install -r requirements.txt
