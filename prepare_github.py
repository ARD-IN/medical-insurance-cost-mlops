"""
Prepare project for GitHub upload
"""
import os
import shutil
from pathlib import Path

def create_gitignore():
    """Create comprehensive .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb

# Environment variables
.env
.env.local

# Data files (tracked by DVC)
data/raw/*.csv
data/processed/*.csv
data/processed/*.pkl

# Models (tracked by DVC)
models/*.pkl
models/*.joblib
models/*.h5

# MLflow
mlruns/
mlartifacts/

# DVC
.dvc/cache
.dvc/tmp

# Logs
*.log
logs/
*.out

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover

# Testing
.pytest_cache/
.tox/

# Documentation builds
docs/_build/

# Large files
*.zip
*.tar.gz
*.rar

# OS files
Thumbs.db
desktop.ini

# Kaggle credentials (IMPORTANT!)
kaggle.json
.kaggle/

# Metrics and plots (can be regenerated)
metrics/plots/*.png
metrics/plots/*.jpg

# Temporary files
*.tmp
*.temp
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✓ Created .gitignore")

def create_license():
    """Create MIT License"""
    license_content = """MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open('LICENSE', 'w') as f:
        f.write(license_content)
    
    print("✓ Created LICENSE")

def create_github_actions():
    """Create GitHub Actions workflow"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    ci_workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint with flake8
      run: |
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  docker:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/insurance-api:latest
          ${{ secrets.DOCKER_USERNAME }}/insurance-api:${{ github.sha }}
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/insurance-api:buildcache
        cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/insurance-api:buildcache,mode=max
"""
    
    with open(workflow_dir / 'ci-cd.yml', 'w') as f:
        f.write(ci_workflow)
    
    print("✓ Created GitHub Actions workflow")

def create_contributing_guide():
    """Create CONTRIBUTING.md"""
    contributing = """# Contributing to Medical Insurance Cost MLOps

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](../../issues)
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information

### Suggesting Features

1. Check [Issues](../../issues) for similar suggestions
2. Create a new issue describing:
   - The problem you're trying to solve
   - Your proposed solution
   - Why this would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/medical-insurance-cost-mlops.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small
- Add comments for complex logic

## Commit Message Guidelines

```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat: Add confidence interval to predictions

Implement bootstrap method for confidence intervals.
Add new endpoint /predict_with_confidence.

Closes #123
```

## Testing

- Write tests for new features
- Maintain test coverage above 80%
- Test edge cases
- Use meaningful test names

## Questions?

Feel free to open an issue or contact the maintainers.

Thank you for contributing! 🚀
"""
    
    with open('CONTRIBUTING.md', 'w') as f:
        f.write(contributing)
    
    print("✓ Created CONTRIBUTING.md")

def create_code_of_conduct():
    """Create CODE_OF_CONDUCT.md"""
    code_of_conduct = """# Code of Conduct

## Our Pledge

We are committed to providing a welcoming and inspiring community for all.

## Our Standards

Examples of behavior that contributes to creating a positive environment:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior:

* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information without explicit permission
* Other conduct which could reasonably be considered inappropriate

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated promptly and fairly.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org), version 2.0.
"""
    
    with open('CODE_OF_CONDUCT.md', 'w') as f:
        f.write(code_of_conduct)
    
    print("✓ Created CODE_OF_CONDUCT.md")

def clean_unnecessary_files():
    """Clean up files that shouldn't be in GitHub"""
    unnecessary = [
        'check_docker.py',
        'stop_local_api.py',
        'manage_container.py',
        'docker_deploy.py',
        'prepare_github.py',  # This file itself
    ]
    
    for file in unnecessary:
        if Path(file).exists():
            print(f"  Remove {file}? (Optional utility script)")

def check_sensitive_data():
    """Check for sensitive data"""
    print("\n" + "="*70)
    print("Checking for sensitive data...")
    print("="*70)
    
    sensitive_files = [
        'kaggle.json',
        '.env',
        '.kaggle/kaggle.json'
    ]
    
    found_sensitive = []
    for file in sensitive_files:
        if Path(file).exists():
            found_sensitive.append(file)
    
    if found_sensitive:
        print("\n⚠️  WARNING: Sensitive files found!")
        for file in found_sensitive:
            print(f"   - {file}")
        print("\nThese files are in .gitignore and won't be uploaded.")
        print("Make sure they're not tracked: git status")
    else:
        print("✓ No sensitive files found")

def main():
    """Main preparation function"""
    print("="*70)
    print("PREPARING PROJECT FOR GITHUB")
    print("="*70)
    
    # Create necessary files
    create_gitignore()
    create_license()
    create_github_actions()
    create_contributing_guide()
    create_code_of_conduct()
    
    # Check for issues
    check_sensitive_data()
    
    print("\n" + "="*70)
    print("✓ Project prepared for GitHub!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review all files: git status")
    print("2. Initialize git: git init")
    print("3. Add files: git add .")
    print("4. Commit: git commit -m 'Initial commit'")
    print("5. Add remote: git remote add origin <your-repo-url>")
    print("6. Push: git push -u origin main")
    
    print("\nOr use the upload script:")
    print("  python upload_to_github.py")

if __name__ == "__main__":
    main()