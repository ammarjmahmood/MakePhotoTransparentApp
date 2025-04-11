@echo off
setlocal enabledelayedexpansion

REM Get the directory where the batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Starting Windows build process from: %CD%

REM Check if running from correct directory
if not exist "transparent_bg_app.py" (
    echo Error: transparent_bg_app.py not found!
    echo Please make sure all files are in the same directory as this script.
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Download from: https://www.python.org/downloads/windows/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check required files
echo Checking required files...
set MISSING_FILES=0
for %%F in (transparent_bg_app.py requirements.txt create_icon.py installer.iss) do (
    if not exist "%%F" (
        echo Error: %%F is missing!
        set /a MISSING_FILES+=1
    )
)
if !MISSING_FILES! neq 0 (
    echo One or more required files are missing. Please check the files above.
    pause
    exit /b 1
)

REM Remove old virtual environment if exists
if exist "venv" (
    echo Removing old virtual environment...
    rmdir /s /q "venv"
)

REM Check if Inno Setup is installed
echo Checking for Inno Setup...
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1" >nul 2>&1
if errorlevel 1 (
    echo Downloading Inno Setup...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://files.jrsoftware.org/is/6/innosetup-6.2.2.exe' -OutFile 'innosetup.exe'}"
    if not exist "innosetup.exe" (
        echo Error: Failed to download Inno Setup!
        pause
        exit /b 1
    )
    echo Installing Inno Setup...
    start /wait innosetup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
    del innosetup.exe
)

REM Create and activate virtual environment
echo Creating virtual environment...
python -m venv "%CD%\venv"
if errorlevel 1 (
    echo Error: Failed to create virtual environment!
    pause
    exit /b 1
)

echo Activating virtual environment...
call "%CD%\venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Error: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
python -m pip install --upgrade pip
python -m pip install requests pyinstaller
python -m pip install -r "%CD%\requirements.txt"
if errorlevel 1 (
    echo Error: Failed to install requirements!
    pause
    exit /b 1
)

REM Generate icon
echo Generating application icon...
python "%CD%\create_icon.py"
if errorlevel 1 (
    echo Error: Failed to generate icon!
    pause
    exit /b 1
)

REM Download model if not exists
if not exist "u2net.onnx" (
    echo Downloading U2Net model...
    python -c "import requests; open('u2net.onnx', 'wb').write(requests.get('https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx').content)"
    if errorlevel 1 (
        echo Error: Failed to download U2Net model!
        pause
        exit /b 1
    )
)

REM Build executable
echo Building executable...
python -m PyInstaller --onefile --add-data "u2net.onnx;." --icon "icon.ico" --name "transparent_bg" transparent_bg_app.py
if errorlevel 1 (
    echo Error: Failed to build executable!
    pause
    exit /b 1
)

REM Check if Inno Setup executable exists
set ISCC_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC_PATH% (
    set ISCC_PATH="C:\Program Files\Inno Setup 6\ISCC.exe"
)
if not exist %ISCC_PATH% (
    echo Error: Cannot find Inno Setup Compiler!
    echo Please make sure Inno Setup 6 is installed correctly.
    pause
    exit /b 1
)

REM Create installer
echo Creating installer...
%ISCC_PATH% "%CD%\installer.iss"
if errorlevel 1 (
    echo Error: Failed to create installer!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo You can find:
echo - Executable at: %CD%\dist\transparent_bg.exe
echo - Installer at: %CD%\installer\BackgroundRemover_Setup.exe
echo.
pause 