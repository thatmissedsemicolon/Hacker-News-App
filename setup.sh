#!/bin/bash

# Function to install necessary dependencies to run the web app
setup_environment() {
    echo "Installing necessary dependencies..."

    # Printing out the python version
    python3 -V 

    # Set up Virtual Environment
    python3 -m venv .venv

    # Activate the environment
    . .venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip

    # Install the requirements
    pip install -r requirements.txt

    # Add Current working directory to the .env file
    echo "APP_SECRET_KEY=$(python3 -c 'import os; print(os.urandom(32).hex())')" >> .env
    echo "SQL_DIR=$(pwd)/database" >> .env
    echo "SQL_BACKUP_DIR=$(pwd)/db_backups" >> .env
}

# start the local server
start_local_server() {
    # Activate the environment
    . .venv/bin/activate

    # Starts the server
    python3 fetch_news.py && python3 app.py 
}

# deploy to ubuntu
deploy_to_ubuntu_server() {
    # gitlab host
    ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
  
    # clone the new repo contents
    if [ -d /home/sury/pythonserver ]; then
        # Navigating to the repo
        cd pythonserver
        
        # pulling the changes
        git pull origin main

        # Reload the application using Supervisor
        sudo supervisorctl reload
    else
        # pulling the repo 
        git clone git@github.com:thatmissedsemicolon/Hacker-News-App.git

        # Navigating to the latest repo
        cd pythonserver

        # Run your setup script
        bash setup.sh install

        # Reload the application using Supervisor
        sudo supervisorctl reload
    fi
}

# Function to run tests using pylint
run_pylint_tests() {
    echo "Running Pylint tests..."

    # Activate the virtual environment
    . .venv/bin/activate

    # Run pylint on all Python files
    find . -type d \( -name .venv -o -name __pycache__ -o -name .pytest_cache \) -prune -false -o -type f -name "*.py" -exec pylint {} +
}

# Function to run tests with pytest using coverage
run_coverage_pytest_tests() {
    echo "Running test with pytest using coverage..."

    # Activate the virtual environment
    . .venv/bin/activate

    # Run tests with coverage
    coverage run -m pytest tests/test_routes.py tests/test_server.py
    coverage report -m
}

# Function to install Python on ubuntu
install_python_ubuntu() {
    apt update && apt upgrade -y
    apt-get install python3 -y
    apt install python3.10-venv -y
    python3 -V
}

# Function to install Homebrew and Python on macOS
install_brew_and_python_mac() {
    which brew || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew update && brew upgrade
    brew install python3
}

# Function to display usage
usage() {
    echo "Usage: $0 [ubuntu|mac|install|deploy|start|pylint|coverage]"
    exit 1
}

# Checks if an argument is provided
if [ $# -eq 0 ]; then
    usage
fi

# Checks the argument and calls the appropriate function
case $1 in
    ubuntu)
        install_python_ubuntu
        ;;
    mac)
        install_brew_and_python_mac
        ;;
    install)
        setup_environment
        ;;
    deploy)
        deploy_to_ubuntu_server
        ;;
    start)
        start_local_server
        ;;
    pylint)
        run_pylint_tests
        ;;
    coverage)
        run_coverage_pytest_tests
        ;;
    *)
        usage
        ;;
esac

