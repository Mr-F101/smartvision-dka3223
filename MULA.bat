@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Jalankan SETUP.bat terlebih dahulu.
 pause
 exit /b 1
)
echo Buka http://127.0.0.1:8000 dalam pelayar. Tekan Ctrl+C untuk henti.
".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
