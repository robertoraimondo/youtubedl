@echo off
echo Building YouTube Downloader executable...
echo.

REM Install PyInstaller if not already installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Creating executable with PyInstaller...
pyinstaller --onefile --windowed --name "YouTube_Downloader" --icon="Youtube-icon.ico" --add-data "proxy_list.txt;." youtube_downloader_gui.py

echo.
if exist dist\YouTube_Downloader.exe (
    echo ============================================
    echo BUILD SUCCESSFUL!
    echo ============================================
    echo.
    echo Executable location: dist\YouTube_Downloader.exe
    echo.
    echo IMPORTANT: Remember to place these files in the same folder:
    echo   - cookies.txt (export using the cookie wizard)
    echo   - proxy_list.txt (already included)
    echo   - FFmpeg must be installed on the system
    echo.
    echo Press any key to open the dist folder...
    pause >nul
    explorer dist
) else (
    echo.
    echo BUILD FAILED! Check the output above for errors.
    echo.
    pause
)
