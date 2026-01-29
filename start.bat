@echo off
echo Starting Course Companion FTE development servers...

REM Start backend server in a new window
start cmd /k "cd /d backend && python -m uvicorn main:app --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server in a new window
start cmd /k "cd /d frontend && npm run dev"

echo Servers started. Backend: http://127.0.0.1:8000, Frontend: http://localhost:3000
pause