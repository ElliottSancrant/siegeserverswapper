@echo off
echo Cleaning previous build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo Clean complete!
pause

