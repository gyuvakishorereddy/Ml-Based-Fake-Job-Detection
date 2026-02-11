#!/usr/bin/env python
"""
Setup script for Fraud Detection System
Automates installation and initial setup
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60 + "\n")

def print_step(step_num, text):
    print(f"\n[Step {step_num}] {text}")
    print("-" * 60)

def run_command(command, description=""):
    """Run a system command"""
    if description:
        print(f"\n{description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(f"Success: {result.stdout[:200]}")
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    print_header("FRAUD DETECTION SYSTEM - SETUP")
    print("Welcome! This script will help you set up the application.\n")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("ERROR: Python 3.8+ is required!")
        sys.exit(1)
    print("✓ Python version is compatible")
    
    # Step 2: Create project structure
    print_step(2, "Creating Project Structure")
    directories = [
        'models',
        'templates',
        'static/css',
        'static/js',
        'static/images'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Step 3: Create virtual environment (optional)
    print_step(3, "Virtual Environment")
    venv_dir = 'venv'
    
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in '{venv_dir}'...")
        if platform.system() == "Windows":
            subprocess.run([sys.executable, "-m", "venv", venv_dir])
        else:
            subprocess.run([sys.executable, "-m", "venv", venv_dir])
        print(f"✓ Virtual environment created")
        
        # Print activation instructions
        print("\nActivate virtual environment:")
        if platform.system() == "Windows":
            print(f"  {venv_dir}\\Scripts\\activate")
        else:
            print(f"  source {venv_dir}/bin/activate")
    else:
        print(f"✓ Virtual environment already exists at '{venv_dir}'")
    
    # Step 4: Install dependencies
    print_step(4, "Installing Dependencies")
    
    if os.path.exists('requirements.txt'):
        print("Installing packages from requirements.txt...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=False
        )
        
        if result.returncode == 0:
            print("\n✓ Dependencies installed successfully")
        else:
            print("\n⚠ There were some issues installing dependencies")
            print("  Try running manually: pip install -r requirements.txt")
    else:
        print("ERROR: requirements.txt not found!")
        sys.exit(1)
    
    # Step 5: Train models
    print_step(5, "Training Models")
    print("\nWould you like to train the ML models now?")
    print("This will generate synthetic datasets and train all models.")
    print("It may take 5-10 minutes depending on your system.")
    
    response = input("\nTrain models now? (y/n): ").strip().lower()
    
    if response == 'y':
        print("\nStarting model training...")
        result = subprocess.run([sys.executable, "train_models.py"])
        
        if result.returncode == 0:
            print("\n✓ Models trained successfully")
        else:
            print("\n⚠ There were issues training models")
            print("  Try running manually: python train_models.py")
    else:
        print("\nYou can train models later by running: python train_models.py")
    
    # Step 6: Verify setup
    print_step(6, "Verifying Setup")
    
    required_files = [
        'app.py',
        'train_models.py',
        'requirements.txt',
        'config.py',
        'templates/index.html',
        'static/css/style.css',
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_good = False
    
    if all_good:
        print("\n✓ All required files are present!")
    else:
        print("\n⚠ Some files are missing. Please check your setup.")
    
    # Final instructions
    print_header("SETUP COMPLETE!")
    
    print("""
To start the application:

1. Activate virtual environment (if you created one):
   - Windows: venv\\Scripts\\activate
   - macOS/Linux: source venv/bin/activate

2. Run the Flask application:
   python app.py

3. Open your browser and go to:
   http://localhost:5000

Additional Commands:
- Train models: python train_models.py
- Run tests: python -m pytest (if pytest is installed)

For more information, see README.md

Happy analyzing!
""")

if __name__ == '__main__':
    main()
