#!/bin/bash
echo "Stopping beets-viz..."
pkill -f "uvicorn main:app.*8000" 2>/dev/null
pkill -f "vite.*5173" 2>/dev/null
echo "Done"
