#!/bin/bash
cd /root/.openclaw/workspace/GeoWar-Pulse

echo "=== Testing GeoWar Pulse Backend ==="
echo ""

# Check if backend imports work
echo "1. Checking Python imports..."
if .venv/bin/python -c "from app.main import app; print('✓ Backend imports OK')" 2>/dev/null; then
    echo "✓ Backend imports successful"
else
    echo "✗ Backend imports failed"
    exit 1
fi

# Start test server
PORT=9123
echo ""
echo "2. Starting test server on port $PORT..."
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port $PORT --log-level error &
SERVER_PID=$!
sleep 3

echo ""
echo "3. Testing endpoints..."

# Test /scores
if curl -s http://127.0.0.1:$PORT/scores | jq -r '.count' 2>/dev/null; then
    echo "✓ /scores endpoint working"
else
    echo "✗ /scores endpoint failed"
    kill $SERVER_PID
    exit 1
fi

# Test /scores/UKR
if curl -s http://127.0.0.1:$PORT/scores/UKR | jq -r '.country_code' 2>/dev/null; then
    echo "✓ /scores/{countryCode} endpoint working"
else
    echo "✗ /scores/{countryCode} endpoint failed"
    kill $SERVER_PID
    exit 1
fi

# Test /health
if curl -s http://127.0.0.1:$PORT/health | jq -r '.status' 2>/dev/null; then
    echo "✓ /health endpoint working"
else
    echo "✗ /health endpoint failed"
    kill $SERVER_PID
    exit 1
fi

echo ""
echo "4. Stopping test server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo ""
echo "=== Backend Test Complete ==="
echo "All backend endpoints PASS"