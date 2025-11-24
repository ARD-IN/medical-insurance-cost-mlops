"""
Automated GitHub upload script
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        if result.stdout:
            print(result.stdout)
        if result.returncode == 0:
            print(f"✓ {description} completed")
            return True
        else:
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return False

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except:
        print("❌ Git is not installed!")
        print("\nPlease install Git from: https://git-scm.com/downloads")
        return False

def get_repo_url():
    """Get repository URL from user"""
    print("\n" + "="*70)
    print("GitHub Repository Setup")
    print("="*70)
    
    print("\nPlease create a repository on GitHub:")
    print("1. Go to https://github.com/new")
    print("2. Repository name: medical-insurance-cost-mlops")
    print("3. Description: End-to-end MLOps project for medical insurance cost prediction")
    print("4. Choose Public or Private")
    print("5. DO NOT initialize with README")
    print("6. Click 'Create repository'")
    
    repo_url = input("\nEnter your repository URL (e.g., https://github.com/username/repo.git): ").strip()
    
    if not repo_url:
        print("❌ Repository URL is required")
        return None
    
    return repo_url

def configure_git():
    """Configure git user"""
    print("\n" + "="*70)
    print("Git Configuration")
    print("="*70)
    
    # Check if already configured
    try:
        name_result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True
        )
        email_result = subprocess.run(
            ['git', 'config', 'user.email'],
            capture_output=True,
            text=True
        )
        
        if name_result.stdout.strip() and email_result.stdout.strip():
            print(f"✓ Git already configured")
            print(f"  Name: {name_result.stdout.strip()}")
            print(f"  Email: {email_result.stdout.strip()}")
            return True
    except:
        pass
    
    # Configure git
    name = input("\nEnter your name: ").strip()
    email = input("Enter your email: ").strip()
    
    if name and email:
        subprocess.run(['git', 'config', '--global', 'user.name', name])
        subprocess.run(['git', 'config', '--global', 'user.email', email])
        print("✓ Git configured")
        return True
    
    return False

def initialize_git():
    """Initialize git repository"""
    if Path('.git').exists():
        print("\n✓ Git repository already initialized")
        
        reinit = input("Reinitialize? This will remove all git history. (yes/no): ").strip().lower()
        if reinit == 'yes':
            import shutil
            shutil.rmtree('.git')
            run_command('git init', 'Initializing Git repository')
            run_command('git branch -M main', 'Creating main branch')
        return True
    else:
        run_command('git init', 'Initializing Git repository')
        run_command('git branch -M main', 'Creating main branch')
        return True

def create_initial_commit():
    """Create initial commit"""
    print("\n" + "="*70)
    print("Creating Initial Commit")
    print("="*70)
    
    # Check what will be committed
    subprocess.run(['git', 'status'])
    
    proceed = input("\nProceed with commit? (yes/no): ").strip().lower()
    if proceed != 'yes':
        print("Commit cancelled")
        return False
    
    run_command('git add .', 'Staging files')
    run_command('git commit -m "Initial commit: Medical Insurance Cost MLOps Project"', 'Creating commit')
    
    return True

def push_to_github(repo_url):
    """Push to GitHub"""
    print("\n" + "="*70)
    print("Pushing to GitHub")
    print("="*70)
    
    # Add remote
    run_command(f'git remote add origin {repo_url}', 'Adding remote', check=False)
    
    # Or set remote if already exists
    run_command(f'git remote set-url origin {repo_url}', 'Setting remote URL', check=False)
    
    # Push
    print("\nPushing to GitHub...")
    print("You may be prompted for your GitHub credentials.")
    
    result = subprocess.run(
        ['git', 'push', '-u', 'origin', 'main'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Successfully pushed to GitHub!")
        return True
    else:
        print(f"❌ Push failed: {result.stderr}")
        print("\nIf authentication failed, you may need to:")
        print("1. Use Personal Access Token instead of password")
        print("2. Configure SSH key")
        print("3. Use GitHub Desktop")
        return False

def show_success_message(repo_url):
    """Show success message"""
    print("\n" + "="*70)
    print("🎉 PROJECT SUCCESSFULLY UPLOADED TO GITHUB!")
    print("="*70)
    
    # Extract repo name from URL
    repo_name = repo_url.rstrip('.git').split('/')[-1]
    username = repo_url.rstrip('.git').split('/')[-2]
    
    print(f"\n📍 Your repository: https://github.com/{username}/{repo_name}")
    print(f"\n📚 Next steps:")
    print(f"1. Visit your repository: https://github.com/{username}/{repo_name}")
    print(f"2. Add repository description and topics")
    print(f"3. Enable GitHub Actions (if you want CI/CD)")
    print(f"4. Add badges to README")
    print(f"5. Share your project!")
    
    print("\n🔧 Configure GitHub Actions secrets:")
    print("   - DOCKER_USERNAME: Your Docker Hub username")
    print("   - DOCKER_PASSWORD: Your Docker Hub password/token")
    
    print("\n📝 README badges you can add:")
    print(f"   ![Tests](https://github.com/{username}/{repo_name}/actions/workflows/ci-cd.yml/badge.svg)")
    print(f"   ![Python](https://img.shields.io/badge/python-3.10+-blue.svg)")
    print(f"   ![License](https://img.shields.io/badge/license-MIT-green.svg)")

def main():
    """Main upload function"""
    print("\n" + "="*70)
    print("🚀 UPLOAD TO GITHUB")
    print("="*70)
    
    # Step 1: Check git
    if not check_git_installed():
        return False
    
    # Step 2: Configure git
    if not configure_git():
        print("❌ Git configuration failed")
        return False
    
    # Step 3: Get repo URL
    repo_url = get_repo_url()
    if not repo_url:
        return False
    
    # Step 4: Initialize git
    if not initialize_git():
        return False
    
    # Step 5: Create commit
    if not create_initial_commit():
        return False
    
    # Step 6: Push to GitHub
    if not push_to_github(repo_url):
        return False
    
    # Step 7: Success!
    show_success_message(repo_url)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Upload cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)