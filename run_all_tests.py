"""
Run all tests and generate summary
"""
import subprocess
import sys
from pathlib import Path
import os

def run_simple_tests():
    """Run simple diagnostic tests"""
    print("\n" + "="*70)
    print("RUNNING SIMPLE DIAGNOSTIC TESTS")
    print("="*70)
    result = subprocess.run([sys.executable, "test_simple.py"])
    return result.returncode == 0

def run_pytest():
    """Run pytest suite"""
    print("\n" + "="*70)
    print("RUNNING PYTEST SUITE")
    print("="*70)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", 
         "--color=yes", "-x"]  # -x stops at first failure
    )
    return result.returncode == 0

def run_pytest_with_coverage():
    """Run pytest with coverage"""
    print("\n" + "="*70)
    print("RUNNING TESTS WITH COVERAGE")
    print("="*70)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", 
         "--cov=src", "--cov-report=term", "--cov-report=html"]
    )
    return result.returncode == 0

def main():
    """Main test orchestrator"""
    os.chdir(Path(__file__).parent)
    
    print("="*70)
    print("MEDICAL INSURANCE COST - COMPLETE TEST SUITE")
    print("="*70)
    print(f"Working Directory: {os.getcwd()}")
    
    # Step 1: Simple tests
    simple_pass = run_simple_tests()
    
    if not simple_pass:
        print("\n❌ Simple tests failed! Fix basic issues before running pytest.")
        return False
    
    print("\n✓ Simple tests passed!")
    
    # Step 2: Pytest
    pytest_pass = run_pytest()
    
    if not pytest_pass:
        print("\n⚠️  Some pytest tests failed.")
        choice = input("\nRun coverage report anyway? (y/n): ").strip().lower()
        if choice != 'y':
            return False
    
    # Step 3: Coverage
    print("\n" + "="*70)
    print("Generating coverage report...")
    print("="*70)
    coverage_pass = run_pytest_with_coverage()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Simple Tests:  {'✓ PASS' if simple_pass else '❌ FAIL'}")
    print(f"Pytest Suite:  {'✓ PASS' if pytest_pass else '❌ FAIL'}")
    print(f"Coverage:      {'✓ Generated' if coverage_pass else '❌ Failed'}")
    
    if coverage_pass:
        coverage_file = Path("htmlcov/index.html")
        if coverage_file.exists():
            print(f"\n📊 Coverage report: {coverage_file.absolute()}")
            print("   Open in browser to view detailed coverage")
    
    print("="*70)
    
    return simple_pass and pytest_pass

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)