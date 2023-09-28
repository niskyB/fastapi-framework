#!/bin/bash

#Preconfig
sudo apt-get update
sudo apt-get -y upgrade

sudo apt-get install python3-dev build-essential
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip in the virtual environment
pip install --upgrade pip

# Install poetry in the virtual environment
pip install poetry

# Install dependencies
poetry install

uvicorn app.main:app --reload