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
echo Letak model_unquant.tflite dan labels.txt di models\tflite.
echo Mulakan semula server melalui MULA.bat.
pause
