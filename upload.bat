@echo off
setlocal

echo Uploading to PyPI...
twine upload dist/*

if errorlevel 1 (
    echo Upload failed!
    exit /b %errorlevel%
)

echo Done.
endlocal