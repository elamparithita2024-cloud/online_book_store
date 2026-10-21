@echo off
title BookVerse - Online Book Store & SCM Portal
color 0B

echo ======================================================================
echo    BOOKVERSE - ONLINE BOOK STORE & SCM INTEGRATED APPLICATION
echo ======================================================================
echo.
echo Select an option:
echo.
echo   [1] Direct Browser Mode (Zero dependencies, instant launch)
echo   [2] Node.js Express REST API Server (http://localhost:3000)
echo   [3] Python Web Server & REST API (http://localhost:8000)
echo   [4] Launch SCM Automation Tool (Git / PySCM)
echo   [5] Open Project in Visual Studio Code
echo   [6] Initialize Git and Push Code (GitHub / GitLab)
echo   [7] Exit
echo.
set /p choice="Enter option (1-7): "

if "%choice%"=="1" (
    echo Opening index.html in your default web browser...
    start "" "index.html"
    goto end
)

if "%choice%"=="2" (
    echo Starting Node.js server...
    start "" "http://localhost:3000"
    node server.js
    goto end
)

if "%choice%"=="3" (
    echo Starting Python server...
    start "" "http://localhost:8000"
    python app.py
    goto end
)

if "%choice%"=="4" (
    python scm_tool.py status
    echo.
    pause
    goto end
)

if "%choice%"=="5" (
    call open_in_vscode.bat
    goto end
)

if "%choice%"=="6" (
    call git_push_setup.bat
    goto end
)

:end
