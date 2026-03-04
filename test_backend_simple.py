#!/usr/bin/env python3
"""Test backend endpoints without httpx dependency"""
import sys
import json
import subprocess
import time
import socket
import signal

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def run_backend_test():
    port = get_free_port()
    print(f"Starting test server on port {port}...")
    
    # Start uvicorn server
    proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", "127.0.0.1", "--port", str(port), "--log-level", "error"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Give server time to start
    time.sleep(2)
    
    try:
        # Test /scores endpoint
        import urllib.request
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}/scores")
            response = urllib.request.urlopen(req, timeout=5)
            data = json.loads(response.read().decode())
            print(f"✓ /scores endpoint returned status {response.status}")
            print(f"  Response keys: {list(data.keys())}")
            print(f"  Count: {data.get('count', 'N/A')}")
            scores_ok = True
        except Exception as e:
            print(f"✗ /scores endpoint failed: {e}")
            scores_ok = False
        
        # Test /scores/UKR endpoint
        try:
            req2 = urllib.request.Request(f"http://127.0.0.1:{port}/scores/UKR")
            response2 = urllib.request.urlopen(req2, timeout=5)
            data2 = json.loads(response2.read().decode())
            print(f"✓ /scores/UKR endpoint returned status {response2.status}")
            print(f"  Country code: {data2.get('country_code', 'N/A')}")
            print(f"  Risk score: {data2.get('risk_score', 'N/A')}")
            country_ok = True
        except Exception as e:
            print(f"✗ /scores/UKR endpoint failed: {e}")
            country_ok = False
        
        # Test /health endpoint
        try:
            req3 = urllib.request.Request(f"http://127.0.0.1:{port}/health")
            response3 = urllib.request.urlopen(req3, timeout=5)
            print(f"✓ /health endpoint returned status {response3.status}")
            health_ok = True
        except Exception as e:
            print(f"✗ /health endpoint failed: {e}")
            health_ok = False
        
        return scores_ok and country_ok and health_ok
        
    finally:
        # Kill server
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    print("Testing GeoWar Pulse backend endpoints...")
    success = run_backend_test()
    sys.exit(0 if success else 1)