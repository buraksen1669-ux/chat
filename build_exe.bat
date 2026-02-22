@echo off
setlocal

where py >nul 2>nul
if %errorlevel% neq 0 (
  echo [HATA] Python Launcher (py) bulunamadi. Python 3.10+ kurulu oldugundan emin olun.
  exit /b 1
)

echo [1/3] Sanal ortam olusturuluyor...
py -3 -m venv .venv
if %errorlevel% neq 0 exit /b 1

call .venv\Scripts\activate.bat

echo [2/3] Gerekli paketler kuruluyor...
python -m pip install --upgrade pip >nul
python -m pip install pyinstaller
if %errorlevel% neq 0 exit /b 1

echo [3/3] EXE paketi olusturuluyor...
pyinstaller --noconfirm --clean --onefile --windowed --name InstaPilot app.py
if %errorlevel% neq 0 exit /b 1

echo.
echo Basarili! EXE dosyasi: dist\InstaPilot.exe
echo.
pause
