"""
Script to start the FastAPI server
"""
import subprocess
import sys
import webbrowser
import time
from pathlib import Path
import os

def check_port_available(port=8000):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def start_server():
    """Start the FastAPI server"""
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    print("="*70)
    print("Starting Medical Insurance Cost Prediction API")
    print("="*70)
    
    # Check if model exists
    if not Path("models/model.pkl").exists():
        print("\n❌ Model not found!")
        print("Please train the model first:")
        print("  python src\\models\\train.py")
        return False
    
    # Check if port is available
    if not check_port_available(8000):
        print("\n⚠️  Port 8000 is already in use!")
        print("Another instance might be running.")
        choice = input("Kill existing process and restart? (y/n): ").strip().lower()
        if choice != 'y':
            return False
    
    print("\n✓ Model found")
    print("✓ Starting server on http://localhost:8000")
    print("\n📚 API Documentation will be available at:")
    print("   http://localhost:8000/docs")
    print("\n⏹️  Press CTRL+C to stop the server\n")
    print("="*70 + "\n")
    
    # Wait a moment then open browser
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:8000/docs")
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start uvicorn
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.api.app:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        return True

if __name__ == "__main__":
    start_server()