"""
Testing and Validation Script
Verifies that the Flask application is set up correctly
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def check_python_version():
    """Check if Python version is 3.8+"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.8+ required (found {version.major}.{version.minor})")
        return False

def check_required_files():
    """Check if all required files exist"""
    print("\nChecking required files...")
    
    required_files = [
        'app.py',
        'train_models.py',
        'config.py',
        'setup.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'templates/index.html',
        'templates/job_detection.html',
        'templates/internship_detection.html',
        'static/css/style.css',
        'static/js/main.js',
        'static/js/job_detection.js',
        'static/js/internship_detection.js',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print_success(file)
        else:
            print_error(f"{file} - MISSING")
            all_exist = False
    
    return all_exist

def check_required_directories():
    """Check if all required directories exist"""
    print("\nChecking required directories...")
    
    required_dirs = [
        'templates',
        'static',
        'static/css',
        'static/js',
        'models',
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print_success(directory)
        else:
            print_error(f"{directory} - MISSING")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if all required Python packages are installed"""
    print("\nChecking Python dependencies...")
    
    required_packages = {
        'flask': 'Flask',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'scikit-learn',
        'xgboost': 'XGBoost',
        'catboost': 'CatBoost',
        'joblib': 'joblib',
    }
    
    all_installed = True
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print_success(f"{package_name}")
        except ImportError:
            print_error(f"{package_name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_trained_models():
    """Check if all trained models exist"""
    print("\nChecking trained models...")
    
    required_models = [
        'models/job_xgboost.pkl',
        'models/job_catboost.pkl',
        'models/job_gradient_boost.pkl',
        'models/job_random_forest.pkl',
        'models/job_decision_tree.pkl',
        'models/job_scaler.pkl',
        'models/internship_svm.pkl',
        'models/internship_random_forest.pkl',
        'models/internship_xgboost.pkl',
        'models/internship_scaler.pkl',
    ]
    
    all_exist = True
    for model in required_models:
        if os.path.exists(model):
            print_success(model)
        else:
            print_warning(f"{model} - NOT FOUND (Run: python train_models.py)")
            all_exist = False
    
    if not all_exist:
        print_warning("Models not trained. Run 'python train_models.py' to train.")
    
    return all_exist

def check_flask_app():
    """Verify Flask app can be imported"""
    print("\nChecking Flask application...")
    
    try:
        sys.path.insert(0, os.getcwd())
        import app
        print_success("Flask app imports successfully")
        return True
    except Exception as e:
        print_error(f"Flask app import failed: {e}")
        return False

def validate_html_templates():
    """Check if HTML templates are valid"""
    print("\nValidating HTML templates...")
    
    templates = [
        'templates/index.html',
        'templates/job_detection.html',
        'templates/internship_detection.html',
    ]
    
    all_valid = True
    for template in templates:
        if os.path.exists(template):
            with open(template, 'r') as f:
                content = f.read()
                if '<html' in content.lower() and '</html>' in content.lower():
                    print_success(f"{template} - Valid HTML structure")
                else:
                    print_warning(f"{template} - May not be valid HTML")
                    all_valid = False
        else:
            print_error(f"{template} - NOT FOUND")
            all_valid = False
    
    return all_valid

def validate_config():
    """Check if config.py is valid"""
    print("\nValidating configuration...")
    
    try:
        import config
        if hasattr(config, 'Config'):
            print_success("Config class found")
            if hasattr(config, 'config'):
                print_success("Config dictionary found")
                return True
            else:
                print_error("Config dictionary not found")
                return False
        else:
            print_error("Config class not found")
            return False
    except Exception as e:
        print_error(f"Config validation failed: {e}")
        return False

def summarize_results(checks):
    """Print summary of all checks"""
    print_header("VALIDATION SUMMARY")
    
    passed = sum(1 for c in checks.values() if c)
    total = len(checks)
    
    print(f"Passed: {Colors.GREEN}{passed}/{total}{Colors.END}\n")
    
    for check_name, result in checks.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"[{status}] {check_name}")
    
    if passed == total:
        print_success("All checks passed! Application is ready.")
        return True
    else:
        failed = total - passed
        print_warning(f"{failed} check(s) failed. See details above.")
        return False

def main():
    print_header("FRAUD DETECTION SYSTEM - VALIDATION")
    
    checks = {
        'Python Version (3.8+)': check_python_version(),
        'Required Files': check_required_files(),
        'Required Directories': check_required_directories(),
        'Python Dependencies': check_dependencies(),
        'Flask Application Import': check_flask_app(),
        'HTML Templates Valid': validate_html_templates(),
        'Configuration Valid': validate_config(),
        'Trained Models': check_trained_models(),
    }
    
    success = summarize_results(checks)
    
    print("\n" + "="*60)
    if success:
        print("""
Next Steps:
1. Start the Flask app: python app.py
2. Open browser: http://localhost:5000
3. Try the detection forms

For detailed information, see README.md and QUICKSTART.md
        """)
    else:
        print("""
Next Steps:
1. Fix the failed checks listed above
2. Run this validation script again
3. For help, see README.md and QUICKSTART.md

Common fixes:
- Missing dependencies: pip install -r requirements.txt
- Missing models: python train_models.py
- File issues: check file names and paths
        """)
    
    print("="*60)
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
