@echo off
title Git SCM - Push to Remote (GitHub / GitLab / VS Code)
color 0B

echo ======================================================================
echo    GIT SCM - INITIALIZE, COMMIT AND PUSH CODE
echo ======================================================================
echo.

:: 1. Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not found in your system PATH!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b
)

:: 2. Initialize Git if not already done
if not exist ".git" (
    echo [1/5] Initializing Git repository...
    git init
) else (
    echo [1/5] Git repository already initialized.
)

:: 3. Configure branch name
echo [2/5] Setting default branch to 'main'...
git branch -M main

:: 4. Stage and commit files
echo [3/5] Staging files and creating initial commit...
git add .
git commit -m "feat: initial commit of online book store application and SCM toolchain"

echo.
echo [4/5] Repository status:
git status -s
echo.

:: 5. Remote Push Option
echo ======================================================================
echo    PUSH TO REMOTE REPOSITORY (GitHub / GitLab / Bitbucket)
echo ======================================================================
echo.
echo Would you like to push this repository to GitHub or GitLab right now?
echo.
set /p pushchoice="Enter remote repository URL (or press ENTER to skip): "

if "%pushchoice%"=="" (
    echo.
    echo [INFO] Skipped remote push. Your local Git repository is completely ready!
    echo You can open it in VS Code by running: open_in_vscode.bat
    echo or using VS Code's Source Control tab (Ctrl+Shift+G).
    echo.
    pause
    exit /b
)

echo.
echo Adding remote origin: %pushchoice%
git remote remove origin >nul 2>nul
git remote add origin %pushchoice%

echo Pushing code to %pushchoice% on branch main...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo  [SUCCESS] Code successfully pushed to remote repository!
    echo ======================================================================
) else (
    echo.
    echo [NOTE] Push failed. Make sure:
    echo   1. The repository exists on GitHub/GitLab.
    echo   2. You are authenticated (run 'git config --global user.name' and sign in).
)

echo.
pause
