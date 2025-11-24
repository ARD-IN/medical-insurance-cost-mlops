"""
Container management script
"""
import subprocess
import sys

def run_cmd(cmd, description=None):
    """Run command and return result"""
    if description:
        print(f"\n{description}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

def container_exists(name="insurance-api"):
    """Check if container exists"""
    result = subprocess.run(
        f"docker ps -a --filter name={name} --format '{{{{.Names}}}}'",
        shell=True,
        capture_output=True,
        text=True
    )
    return name in result.stdout

def container_running(name="insurance-api"):
    """Check if container is running"""
    result = subprocess.run(
        f"docker ps --filter name={name} --format '{{{{.Names}}}}'",
        shell=True,
        capture_output=True,
        text=True
    )
    return name in result.stdout

def show_menu():
    """Show management menu"""
    print("\n" + "="*70)
    print("DOCKER CONTAINER MANAGER")
    print("="*70)
    
    exists = container_exists()
    running = container_running()
    
    print(f"\nContainer Status:")
    print(f"  Exists:  {'✓ Yes' if exists else '❌ No'}")
    print(f"  Running: {'✓ Yes' if running else '❌ No'}")
    
    print("\nAvailable Actions:")
    print("1. Start container")
    print("2. Stop container")
    print("3. Restart container")
    print("4. Remove container")
    print("5. View logs")
    print("6. View status")
    print("7. Create new container (port 8001)")
    print("8. Test API")
    print("9. Exit")
    
    return input("\nSelect action (1-9): ").strip()

def start_container():
    """Start container"""
    if not container_exists():
        print("\n❌ Container doesn't exist. Use option 7 to create it.")
        return False
    
    if container_running():
        print("\n✓ Container is already running")
        return True
    
    return run_cmd("docker start insurance-api", "Starting container...")

def stop_container():
    """Stop container"""
    if not container_running():
        print("\n✓ Container is not running")
        return True
    
    return run_cmd("docker stop insurance-api", "Stopping container...")

def restart_container():
    """Restart container"""
    return run_cmd("docker restart insurance-api", "Restarting container...")

def remove_container():
    """Remove container"""
    if not container_exists():
        print("\n✓ Container doesn't exist")
        return True
    
    confirm = input("\n⚠️  Are you sure you want to remove the container? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled")
        return False
    
    return run_cmd("docker rm -f insurance-api", "Removing container...")

def view_logs():
    """View container logs"""
    if not container_exists():
        print("\n❌ Container doesn't exist")
        return False
    
    print("\n" + "="*70)
    print("Container Logs (last 50 lines)")
    print("="*70)
    run_cmd("docker logs --tail 50 insurance-api")
    
    follow = input("\nFollow logs in real-time? (y/n): ").strip().lower()
    if follow == 'y':
        print("\nPress Ctrl+C to stop following logs\n")
        try:
            subprocess.run("docker logs -f insurance-api", shell=True)
        except KeyboardInterrupt:
            print("\n")
    
    return True

def view_status():
    """View container status"""
    print("\n" + "="*70)
    print("Container Details")
    print("="*70)
    run_cmd("docker ps -a --filter name=insurance-api")
    
    if container_running():
        print("\n" + "="*70)
        print("Container Stats")
        print("="*70)
        run_cmd("docker stats --no-stream insurance-api")
    
    return True

def create_container():
    """Create new container"""
    if container_exists():
        print("\n⚠️  Container already exists")
        remove = input("Remove existing container? (yes/no): ").strip().lower()
        if remove == 'yes':
            remove_container()
        else:
            return False
    
    port = input("\nEnter port to use (default 8001): ").strip() or "8001"
    
    from pathlib import Path
    pwd = Path.cwd()
    
    cmd = f"""docker run -d \
        --name insurance-api \
        -p {port}:8000 \
        -v "{pwd}/models:/app/models:ro" \
        -v "{pwd}/data/processed:/app/data/processed:ro" \
        --restart unless-stopped \
        medical_insurance_cost-api:latest"""
    
    if run_cmd(cmd, f"Creating container on port {port}..."):
        print(f"\n✓ Container created successfully!")
        print(f"\n📍 API available at: http://localhost:{port}")
        print(f"📚 Documentation at: http://localhost:{port}/docs")
        return True
    
    return False

def test_api():
    """Test API"""
    import requests
    import time
    
    # Find which port the container is using
    result = subprocess.run(
        "docker port insurance-api 8000",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and result.stdout:
        port = result.stdout.split(':')[1].strip()
    else:
        port = "8000"
    
    url = f"http://localhost:{port}/health"
    
    print(f"\nTesting API at {url}...")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"\n✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        
        test_pred = input("\nRun test prediction? (y/n): ").strip().lower()
        if test_pred == 'y':
            pred_data = {
                "age": 35,
                "sex": "male",
                "bmi": 27.5,
                "children": 2,
                "smoker": "no",
                "region": "northwest"
            }
            
            pred_response = requests.post(
                f"http://localhost:{port}/predict",
                json=pred_data
            )
            
            print(f"\n✓ Prediction: ${pred_response.json()['predicted_cost']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main menu loop"""
    while True:
        try:
            choice = show_menu()
            
            if choice == '1':
                start_container()
            elif choice == '2':
                stop_container()
            elif choice == '3':
                restart_container()
            elif choice == '4':
                remove_container()
            elif choice == '5':
                view_logs()
            elif choice == '6':
                view_status()
            elif choice == '7':
                create_container()
            elif choice == '8':
                test_api()
            elif choice == '9':
                print("\nExiting...")
                break
            else:
                print("\n❌ Invalid choice")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()