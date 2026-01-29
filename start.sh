#!/bin/bash
# Script to start both backend and frontend servers

echo "Starting Course Companion FTE development servers..."

# Start backend in background
echo "Starting backend server..."
cd backend
python -m uvicorn main:app --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID