@echo off
title Open Project in VS Code
color 0A

echo ======================================================================
echo    LAUNCHING ONLINE BOOK STORE IN VISUAL STUDIO CODE
echo ======================================================================
echo.
echo Opening folder: %~dp0
echo.

code "%~dp0"
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] VS Code opened successfully!
) else (
    echo [NOTE] 'code' command was not found in your system PATH.
    echo Opening folder in Windows Explorer so you can right-click 'Open with Code'...
    explorer "%~dp0"
)

timeout /t 3 >nul
