@echo off
echo ============================================
echo TradingView MCP Server - Installation Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

REM Install required packages
python -m pip install --upgrade pip
python -m pip install mcp tradingview-ta requests

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install packages.
    echo Please try running this script as Administrator.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Open the Claude Desktop config file:
echo    Press Win+R and type: %%APPDATA%%\Claude
echo.
echo 2. Edit or create 'claude_desktop_config.json' with:
echo.
echo {
echo   "mcpServers": {
echo     "tradingview": {
echo       "command": "python",
echo       "args": ["%~dp0server.py"]
echo     }
echo   }
echo }
echo.
echo 3. Restart Claude Desktop
echo.
echo ============================================
pause
