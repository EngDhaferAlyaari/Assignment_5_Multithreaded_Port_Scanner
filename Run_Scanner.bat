@echo off
cd /d "%~dp0"
echo Assignment 5 - Port Scanner (localhost example)
echo.
if exist Port_Scanner.exe (
    Port_Scanner.exe 127.0.0.1 --start 1 --end 1024 --workers 50 --timeout 0.5
) else (
    py -3 port_scanner.py 127.0.0.1 --start 1 --end 1024 --workers 50 --timeout 0.5
)
echo.
pause
