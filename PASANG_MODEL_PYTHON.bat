@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Jalankan SETUP.bat terlebih dahulu.
 pause
 exit /b 1
)
".venv\Scripts\python.exe" -m pip install -r requirements-model.txt
if errorlevel 1 (
 echo Pemasangan gagal. Simpan mesej ralat untuk semakan.
 pause
 exit /b 1
)
".venv\Scripts\python.exe" tools\verify_install.py
if errorlevel 1 exit /b 1
echo Model E2 dan runtime Python telah disahkan.
echo Mulakan semula server melalui MULA.bat.
pause
