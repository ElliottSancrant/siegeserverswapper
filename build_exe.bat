@echo off
echo Building saunis server swapper executable...
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build optimized executable
pyinstaller --onefile --windowed --name "R6ServerChanger" --icon=NONE ^
    --hidden-import selenium ^
    --hidden-import selenium.webdriver ^
    --hidden-import selenium.webdriver.chrome ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module scipy ^
    --exclude-module PIL ^
    --noupx ^
    main.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
echo Package size: ~50-80MB
echo Note: Users need Chrome browser installed for Selenium to work.
echo.
pause

