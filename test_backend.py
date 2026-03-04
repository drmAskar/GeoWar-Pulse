#!/usr/bin/env python3
"""Test backend endpoints"""
import sys
from app.main import app
from fastapi.testclient import TestClient

def main():
    client = TestClient(app)
    
    print("Testing /scores...")
    r = client.get("/scores")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Response keys: {list(data.keys())}")
        print(f"Count: {data.get('count', 'N/A')}")
        print("✓ Backend /scores working")
    else:
        print(f"✗ Backend /scores returned {r.status_code}: {r.text}")
    
    print("\nTesting /scores/UKR...")
    r2 = client.get("/scores/UKR")
    print(f"Status: {r2.status_code}")
    if r2.status_code == 200:
        data2 = r2.json()
        print(f"Country code: {data2.get('country_code', 'N/A')}")
        print(f"Risk score: {data2.get('risk_score', 'N/A')}")
        print("✓ Backend /scores/{countryCode} working")
    else:
        print(f"✗ Backend /scores/UKR returned {r2.status_code}: {r2.text}")
    
    # Test health endpoint
    print("\nTesting /health...")
    r3 = client.get("/health")
    print(f"Status: {r3.status_code}")
    if r3.status_code == 200:
        print("✓ Health check working")
    
    # Test map/snapshot
    print("\nTesting /map/snapshot...")
    r4 = client.get("/map/snapshot")
    print(f"Status: {r4.status_code}")
    if r4.status_code == 200:
        print("✓ Map snapshot working")
    
    return r.status_code == 200 and r2.status_code == 200

if __name__ == "__main__":
    sys.exit(0 if main() else 1)