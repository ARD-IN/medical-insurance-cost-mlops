"""
Check Docker status
"""
import subprocess
import sys

print("="*70)
print("Docker Environment Check")
print("="*70)

# Check Docker installed
print("\n1. Checking if Docker is installed...")
try:
    result = subprocess.run(
        ["docker", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(f"   ✓ {result.stdout.strip()}")
except:
    print("   ❌ Docker not installed or not in PATH")
    sys.exit(1)

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
    else:
        print("   ❌ Docker is not running")
        print("   Please start Docker Desktop")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("   Please start Docker Desktop")
    sys.exit(1)

# Check docker-compose
print("\n3. Checking docker-compose...")
try:
    result = subprocess.run(
        ["docker-compose", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(f"   ✓ {result.stdout.strip()}")
except:
    print("   ❌ docker-compose not available")

print("\n" + "="*70)
print("✓ Docker environment is ready!")
print("="*70)
print("\nYou can now run:")
print("  python docker_build.py")
print("  python docker_deploy.py")