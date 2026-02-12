#!/bin/bash

# Script to install dependencies for the Todo application

echo "Installing backend dependencies..."
cd /mnt/e/7- Q4-HACKATHONS/hackathon2_5-phases_TODO-Application/New/phase-2/backend
pip install -r requirements.txt

echo "Backend dependencies installed."

echo "Installing frontend dependencies..."
cd /mnt/e/7- Q4-HACKATHONS/hackathon2_5-phases_TODO-Application/New/phase-2/frontend

# Due to permission issues in some environments, you may need to run:
# sudo chown -R $(whoami) /mnt/e/7- Q4-HACKATHONS/hackathon2_5-phases_TODO-Application/New/phase-2/frontend
# before running npm install

if [ -d "node_modules" ]; then
    echo "Removing existing node_modules..."
    rm -rf node_modules
fi

echo "Running npm install..."
npm install

if [ $? -ne 0 ]; then
    echo "npm install failed. You may need to run with elevated permissions:"
    echo "sudo chown -R $(whoami) /mnt/e/7- Q4-HACKATHONS/hackathon2_5-phases_TODO-Application/New/phase-2/frontend"
    echo "Then run: npm install"
fi

echo "Frontend dependencies installation attempted."