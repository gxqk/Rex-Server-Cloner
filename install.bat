@echo off
title Rex Server-Cloner - Dependencies Installation
color 9

echo [i] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is not installed or not found in PATH
    echo [i] Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [+] Python detected successfully
echo.

echo [i] Installing dependencies from requirements.txt...
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo [+] Installation completed successfully!
    echo [i] You can now run the program with: python main.py
) else (
    echo.
    echo [X] Error during dependencies installation
    echo [i] Check your internet connection and try again
)

echo.
pause
