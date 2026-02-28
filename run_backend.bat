@echo off
echo Starting Backend Server on Port 8081...
call venv\Scripts\activate.bat
cd backend
echo Environment activated. Starting Uvicorn...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8081
pause
