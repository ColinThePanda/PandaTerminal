@echo off
setlocal

echo Cleaning old builds...
rmdir /S /Q build 2>nul
rmdir /S /Q dist 2>nul
rmdir /S /Q src\panda_terminal.egg-info

echo Building package...
python -m build

if errorlevel 1 (
    echo Build failed!
    exit /b %errorlevel%
)

echo Done.
endlocal