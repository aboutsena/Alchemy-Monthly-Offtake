@echo off
setlocal
cd /d "%~dp0"
"%~dp0runtime\python.exe" -B -X utf8 "%~dp0offtake.py" configure
if errorlevel 1 goto failed
"%~dp0runtime\python.exe" -B -X utf8 "%~dp0offtake.py" doctor
if errorlevel 1 goto failed
echo.
echo Installation verified. Use RUN_OFFTAKE.cmd for the monthly reports.
pause
exit /b 0
:failed
echo Installation needs review. Keep the full message and contact your administrator.
pause
exit /b 2
