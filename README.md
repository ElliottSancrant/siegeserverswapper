# saunis server swapper

A portable Windows application to change the game server for Rainbow Six Siege accounts.

## Features

- Change server for a specific Ubisoft account by username
- Change server for all accounts at once
- Clean, dark mode GUI with purple accent
- Portable .exe file (no installation required)
- Lightweight Python-based application (~50-80MB)

## Building the Executable

### Prerequisites

1. **Python 3.8+** installed
2. **Chrome browser** (users need this installed - Selenium uses it)

### Build Steps

1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

2. Build the executable:
   ```powershell
   build_exe.bat
   ```

   Or manually:
   ```powershell
   pyinstaller --onefile --windowed --name "R6ServerChanger" main.py
   ```

3. The executable will be in the `dist` folder.

### Package Size

- **Executable**: ~21mb 
- **User requirement**: Chrome browser must be installed on target machine

**Note**: ChromeDriver is bundled, but Chrome browser itself must be installed separately by users.

## Usage

1. Run `R6ServerChanger.exe`
2. Enter your Ubisoft username (or check "Skip" to change all accounts)
3. Select your desired server from the dropdown
4. Click "Change Server"
5. The application will:
   - Look up your Ubisoft ID (if username provided)
   - Find your GameSettings.ini file(s)
   - Update the DataCenterHint setting

## Server Options

- Default
- US-West
- US-Central
- US-South-Central
- East-US
- Brazil
- EU-North
- EU-West
- UAE
- South Africa
- Asia-East
- Asia-Southeast
- Japan
- Australia

## Requirements

- Windows OS
- Chrome browser (for Ubisoft ID lookup)
- ChromeDriver (automatically managed by Selenium)

## Notes

- The application requires Chrome/ChromeDriver for Ubisoft ID lookup
- GameSettings.ini files are located in:
  - `C:\Users\<User>\Documents\My Games\Rainbow Six - Siege\<UBISOFT-ID>\GameSettings.ini`
  - `C:\Users\<User>\OneDrive\Documents\My Games\Rainbow Six - Siege\<UBISOFT-ID>\GameSettings.ini`

