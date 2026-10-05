@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo   msiBuilder - OneFile EXE Build
echo   Fachlehrer-DEV
echo ========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python Launcher ^(py^) was not found.
  pause
  exit /b 1
)

py -m pip install --upgrade pyinstaller
if errorlevel 1 (
  echo ERROR: PyInstaller could not be installed or updated.
  pause
  exit /b 1
)

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist msiBuilder.spec del /q msiBuilder.spec

py -m PyInstaller --noconfirm --clean --onefile --windowed --name msiBuilder --icon msibuilder.ico --optimize 2 msibuilder.py
if errorlevel 1 (
  echo.
  echo BUILD FAILED.
  pause
  exit /b 1
)

echo.
echo Done:
echo   %CD%\dist\msiBuilder.exe
echo.
echo msiBuilder checks for the .NET SDK and WiX when started.
echo.
pause
