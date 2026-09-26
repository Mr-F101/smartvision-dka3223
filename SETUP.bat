@echo off
cd /d "%~dp0"
py -3.12 -m venv .venv
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip install -r requirements-model.txt
if errorlevel 1 goto fail
".venv\Scripts\python.exe" tools\verify_install.py
if errorlevel 1 goto fail
echo Setup kedua-dua mod selesai. Jalankan MULA.bat.
pause
exit /b 0
:fail
echo Setup gagal. Pastikan Python 3.12 64 bit dipasang dan internet tersedia.
pause
exit /b 1
