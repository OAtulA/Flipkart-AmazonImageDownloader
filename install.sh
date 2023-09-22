#!/bin/sh

# Check which shell is being used
if [ "$SHELL" = "/bin/bash" ]; then
  echo "You are using Bash"
elif [ "$SHELL" = "/bin/zsh" ]; then
  echo "You are using Zsh"
elif [ "$SHELL" = "/usr/bin/fish" ]; then
  echo "You are using Fish"
else
  echo "Unknown shell"
fi

# Check if venv is installed
if ! command -v python3 >/dev/null 2>&1 || ! python3 -m venv --help >/dev/null 2>&1; then
  echo "venv is not installed. Installing venv..."
  python3 -m pip install --user virtualenv
fi

# Create a virtual environment
if [ ! -d "env" ]; then
  echo "Creating a virtual environment..."
  python3 -m venv env
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
if [ "$SHELL" = "/bin/bash" ] || [ "$SHELL" = "/bin/zsh" ]; then
  . env/bin/activate
elif [ "$SHELL" = "/usr/bin/fish" ]; then
  . env/bin/activate.fish
fi

# Check if virtual environment is activated
if [ -n "$VIRTUAL_ENV" ]; then
  echo "Virtual environment activated"
else
  echo "Virtual environment not activated"
fi

# Making the run.sh executable.
chmod +x run.sh

# Install packages from requirements.txt
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

# Deactivate the virtual environment
echo "Deactivating the virtual environment..."
deactivate

# Check if virtual environment is deactivated
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Virtual environment deactivated"
else
  echo "Virtual environment not deactivated"
fi