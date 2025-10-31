@echo off
echo ========================================
echo NHL Game Predictor - Build Script
echo ========================================
echo.

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Building executable with PyInstaller...
pyinstaller --onefile --windowed --name "NHL_Game_Predictor" --icon=NONE --add-data "src;src" src/main.py

echo.
echo ========================================
echo Build complete!
echo.
echo The .exe file can be found in the 'dist' folder:
echo   dist\NHL_Game_Predictor.exe
echo.
echo You can copy this .exe file anywhere and run it!
echo ========================================
echo.
pause
