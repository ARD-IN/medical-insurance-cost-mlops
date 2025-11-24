"""
Complete Docker deployment script
"""
import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and handle output"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
            shell=True
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
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_docker():
    """Check if Docker is available and running"""
    print("="*70)
    print("Checking Docker Environment")
    print("="*70)
    
    # Check Docker installed
    print("\n1. Checking Docker installation...")
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"   ✓ {result.stdout.strip()}")
    except:
        print("   ❌ Docker not found!")
        print("\nPlease install Docker Desktop from:")
        print("   https://www.docker.com/products/docker-desktop")
        return False
    
    # Check Docker running
    print("\n2. Checking if Docker is running...")
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("   ✓ Docker is running")
            return True
        else:
            print("   ❌ Docker is not running")
            print("\nPlease start Docker Desktop:")
            print("   1. Search for 'Docker Desktop' in Start menu")
            print("   2. Launch Docker Desktop")
            print("   3. Wait for it to fully start (icon in system tray)")
            print("   4. Run this script again")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to Docker: {e}")
        print("\nPlease start Docker Desktop")
        return False

def check_required_files():
    """Check if all required files exist"""
    print("\n" + "="*70)
    print("Checking Required Files")
    print("="*70)
    
    required = {
        "Dockerfile": "Docker configuration",
        "requirements.txt": "Python dependencies",
        "config.yaml": "Application configuration",
        "models/model.pkl": "Trained model",
        "data/processed/scaler.pkl": "Data scaler",
        "data/processed/label_encoders.pkl": "Label encoders"
    }
    
    all_exist = True
    for file, desc in required.items():
        path = Path(file)
        if path.exists():
            size = path.stat().st_size / 1024  # KB
            print(f"✓ {file:40s} ({size:.1f} KB) - {desc}")
        else:
            print(f"❌ {file:40s} - MISSING - {desc}")
            all_exist = False
    
    return all_exist

def cleanup_existing():
    """Clean up existing containers and images"""
    print("\n" + "="*70)
    print("Cleaning Up Existing Resources")
    print("="*70)
    
    # Stop and remove container
    print("\nRemoving old container...")
    subprocess.run(
        ["docker", "stop", "insurance-api"],
        capture_output=True,
        check=False
    )
    subprocess.run(
        ["docker", "rm", "insurance-api"],
        capture_output=True,
        check=False
    )
    print("✓ Cleanup completed")

def build_image():
    """Build Docker image"""
    print("\n" + "="*70)
    print("Building Docker Image")
    print("="*70)
    print("\nThis will take a few minutes on first build...")
    print("Subsequent builds will be faster due to caching.\n")
    
    cmd = "docker build -t medical_insurance_cost-api:latest ."
    return run_command(cmd, "Building image")

def run_container():
    """Run Docker container"""
    print("\n" + "="*70)
    print("Starting Container")
    print("="*70)
    
    # Get current directory for volume mounts
    current_dir = Path.cwd()
    models_path = current_dir / "models"
    data_path = current_dir / "data" / "processed"
    
    cmd = f"""docker run -d \
        --name insurance-api \
        -p 8000:8000 \
        -v "{models_path}:/app/models:ro" \
        -v "{data_path}:/app/data/processed:ro" \
        --restart unless-stopped \
        medical_insurance_cost-api:latest"""
    
    if run_command(cmd, "Starting container"):
        print("\n" + "="*70)
        print("✓ Container Started Successfully!")
        print("="*70)
        return True
    return False

def wait_for_api():
    """Wait for API to be ready"""
    print("\nWaiting for API to start...")
    max_attempts = 30
    
    for i in range(max_attempts):
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✓ API is ready!")
                return True
        except:
            pass
        
        print(f"  Attempt {i+1}/{max_attempts}...", end="\r")
        time.sleep(1)
    
    print("\n⚠️  API did not respond in time")
    return False

def show_status():
    """Show container status and logs"""
    print("\n" + "="*70)
    print("Container Status")
    print("="*70)
    
    # Show container info
    subprocess.run(["docker", "ps", "-a", "--filter", "name=insurance-api"])
    
    print("\n" + "="*70)
    print("Recent Logs")
    print("="*70)
    subprocess.run(["docker", "logs", "--tail", "20", "insurance-api"])

def show_access_info():
    """Show how to access the services"""
    print("\n" + "="*70)
    print("✓ Deployment Complete!")
    print("="*70)
    print("\n📍 Services Available:")
    print("   API:           http://localhost:8000")
    print("   Documentation: http://localhost:8000/docs")
    print("   Health Check:  http://localhost:8000/health")
    
    print("\n📝 Useful Commands:")
    print("   View logs:     docker logs -f insurance-api")
    print("   Stop:          docker stop insurance-api")
    print("   Start:         docker start insurance-api")
    print("   Restart:       docker restart insurance-api")
    print("   Remove:        docker rm -f insurance-api")
    print("   Shell access:  docker exec -it insurance-api /bin/bash")
    
    print("\n🧪 Test API:")
    print('   curl http://localhost:8000/health')
    print('   python test_api_requests.py')
    
    print("\n" + "="*70)

def main():
    """Main deployment function"""
    print("\n" + "="*70)
    print("🐳 DOCKER DEPLOYMENT SCRIPT")
    print("="*70)
    
    # Step 1: Check Docker
    if not check_docker():
        return False
    
    # Step 2: Check files
    if not check_required_files():
        print("\n❌ Missing required files!")
        print("\nPlease ensure you have:")
        print("  1. Trained the model: python src/models/train.py")
        print("  2. Created Dockerfile")
        return False
    
    # Step 3: Cleanup
    cleanup_existing()
    
    # Step 4: Build image
    if not build_image():
        print("\n❌ Failed to build Docker image")
        return False
    
    # Step 5: Run container
    if not run_container():
        print("\n❌ Failed to start container")
        return False
    
    # Step 6: Wait for API
    wait_for_api()
    
    # Step 7: Show status
    show_status()
    
    # Step 8: Show access info
    show_access_info()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)