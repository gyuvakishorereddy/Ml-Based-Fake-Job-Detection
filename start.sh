#!/bin/bash

# Quick Start Script for Linux/Mac
# Run this script to set up and start both backend and frontend

echo "================================"
echo "   ML Scam Detection System    "
echo "   React + Flask Setup          "
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION found${NC}"
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION found${NC}"
    PYTHON_CMD=python
else
    echo -e "${RED}✗ Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if Node.js is installed
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 16+${NC}"
    exit 1
fi

# Ask user what to do
echo ""
echo -e "${CYAN}What would you like to do?${NC}"
echo -e "${NC}1. First-time setup (install dependencies + train models)${NC}"
echo -e "${NC}2. Start servers only (skip setup)${NC}"
echo -e "${NC}3. Exit${NC}"
read -p "Enter your choice (1-3): " choice

if [ "$choice" = "3" ]; then
    exit 0
fi

if [ "$choice" = "1" ]; then
    echo ""
    echo -e "${CYAN}======== BACKEND SETUP ========${NC}"
    
    # Create virtual environment
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install Python dependencies
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install Python dependencies${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
    
    # Train models
    echo -e "${YELLOW}Training ML models (this may take 5-15 minutes)...${NC}"
    $PYTHON_CMD train_models.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to train models${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Models trained successfully${NC}"
    
    echo ""
    echo -e "${CYAN}======== FRONTEND SETUP ========${NC}"
    
    # Install Node dependencies
    echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
    cd frontend
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install Node dependencies${NC}"
        cd ..
        exit 1
    fi
    echo -e "${GREEN}✓ Node dependencies installed${NC}"
    cd ..
    
    echo ""
    echo -e "${GREEN}✓ Setup complete!${NC}"
fi

echo ""
echo -e "${CYAN}======== STARTING SERVERS ========${NC}"
echo -e "${NC}Backend will run on: http://localhost:5000${NC}"
echo -e "${NC}Frontend will run on: http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C in each terminal to stop the servers${NC}"
echo ""

# Start backend in new terminal (using gnome-terminal, xterm, or konsole)
echo -e "${YELLOW}Starting Flask backend...${NC}"
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "source venv/bin/activate; $PYTHON_CMD app.py; exec bash"
elif command -v xterm &> /dev/null; then
    xterm -e "source venv/bin/activate; $PYTHON_CMD app.py; exec bash" &
elif command -v konsole &> /dev/null; then
    konsole -e "source venv/bin/activate; $PYTHON_CMD app.py; exec bash" &
else
    echo -e "${YELLOW}Could not detect terminal. Run manually: $PYTHON_CMD app.py${NC}"
fi

# Wait a bit for backend to start
sleep 3

# Start frontend in new terminal
echo -e "${YELLOW}Starting React frontend...${NC}"
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "cd frontend; npm run dev; exec bash"
elif command -v xterm &> /dev/null; then
    xterm -e "cd frontend; npm run dev; exec bash" &
elif command -v konsole &> /dev/null; then
    konsole -e "cd frontend; npm run dev; exec bash" &
else
    echo -e "${YELLOW}Could not detect terminal. Run manually: cd frontend && npm run dev${NC}"
fi

echo ""
echo -e "${CYAN}================================${NC}"
echo -e "${GREEN}✓ Both servers starting...${NC}"
echo -e "${CYAN}================================${NC}"
echo ""
echo -e "${YELLOW}Open your browser and navigate to:${NC}"
echo -e "${CYAN}http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}Check API health at:${NC}"
echo -e "${CYAN}http://localhost:5000/api/health${NC}"
echo ""
