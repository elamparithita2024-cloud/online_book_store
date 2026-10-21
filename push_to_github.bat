@echo off
title Push Online Book Store to GitHub
color 0A

echo ======================================================================
echo    PUSHING ONLINE BOOK STORE TO GITHUB REPOSITORY
echo    Target: https://github.com/elamparithita2024-cloud/online_book_store.git
echo ======================================================================
echo.

where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not found in your system PATH!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b
)

echo [1/5] Initializing Git repository...
if not exist ".git" (
    git init
)

echo.
echo [2/5] Setting branch to main...
git branch -M main

echo.
echo [3/5] Adding all files to staging...
git add -A

echo.
echo [4/5] Creating commit...
git commit -m "feat: complete online book store application and SCM toolchain"

echo.
echo [5/5] Configuring remote origin...
git remote remove origin >nul 2>nul
git remote add origin https://github.com/elamparithita2024-cloud/online_book_store.git

echo.
echo Pushing to GitHub...
git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo  [SUCCESS] All code pushed successfully to:
    echo  https://github.com/elamparithita2024-cloud/online_book_store
    echo ======================================================================
) else (
    echo.
    echo [NOTE] If prompted for GitHub login, please sign in via browser or
    echo enter your GitHub Personal Access Token.
)

echo.
pause
