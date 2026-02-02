#!/bin/bash
# Start beets-viz development servers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting beets-viz..."

# Kill any existing servers
pkill -f "uvicorn main:app.*8000" 2>/dev/null
pkill -f "vite.*5173" 2>/dev/null
sleep 1

# Start backend
echo "Starting backend on :8000..."
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/beets-viz-backend.log 2>&1 &
sleep 2

# Start frontend
echo "Starting frontend on :5173..."
cd "$SCRIPT_DIR/frontend"
nohup npm run dev -- --host 0.0.0.0 > /tmp/beets-viz-frontend.log 2>&1 &
sleep 3

# Verify
echo ""
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend: http://localhost:8000"
else
    echo "❌ Backend failed to start"
fi

if curl -s http://localhost:5173/ > /dev/null; then
    echo "✅ Frontend: http://localhost:5173"
else
    echo "❌ Frontend failed to start"
fi

echo ""
echo "Logs:"
echo "  Backend:  tail -f /tmp/beets-viz-backend.log"
echo "  Frontend: tail -f /tmp/beets-viz-frontend.log"
