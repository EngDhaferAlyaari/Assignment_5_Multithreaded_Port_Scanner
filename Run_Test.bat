@echo off
cd /d "%~dp0"
echo Assignment 5 - Local Port Scanner Tests
echo.
py -3 -m unittest -v test_port_scanner.py
if errorlevel 1 (
    echo.
    echo If Python is not installed, install Python 3 first.
)
echo.
pause
