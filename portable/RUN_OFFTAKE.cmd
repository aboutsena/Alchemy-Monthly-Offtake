@echo off
setlocal
cd /d "%~dp0"
"%~dp0runtime\python.exe" -B -X utf8 "%~dp0offtake.py" %*
set "offtake_exit=%ERRORLEVEL%"
echo.
pause
exit /b %offtake_exit%
