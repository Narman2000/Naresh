# TradingView MCP Server for Claude AI Desktop

A Model Context Protocol (MCP) server that provides TradingView market data, technical analysis, and trading insights to Claude AI Desktop on Windows 11.

## Features

- **Technical Analysis**: Get comprehensive technical analysis with oscillators, moving averages, and buy/sell/hold recommendations
- **Real-time Quotes**: Fetch current price data for stocks, crypto, and forex
- **Symbol Search**: Search for any tradable instrument on TradingView
- **Market Overview**: View major market indices performance
- **Stock Screener**: Find top gainers, losers, most active, overbought, and oversold stocks
- **Crypto Analysis**: Specialized cryptocurrency technical analysis
- **Forex Analysis**: Currency pair analysis with pivot points

## Prerequisites

- Windows 11 Pro
- Python 3.10 or higher
- Claude Desktop App installed

## Installation on Windows 11

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation by opening Command Prompt and running:
   ```cmd
   python --version
   ```

### Step 2: Download and Setup the MCP Server

1. Create a directory for the MCP server:
   ```cmd
   mkdir C:\Users\%USERNAME%\tradingview-mcp-server
   ```

2. Copy `server.py` and `requirements.txt` to the directory

3. Open Command Prompt as Administrator and navigate to the directory:
   ```cmd
   cd C:\Users\%USERNAME%\tradingview-mcp-server
   ```

4. Create a virtual environment (recommended):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

5. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

### Step 3: Configure Claude Desktop

1. Open the Claude Desktop configuration file. The location is:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

   You can open this in File Explorer by pressing `Win + R` and typing:
   ```
   %APPDATA%\Claude
   ```

2. If the file doesn't exist, create it. Add the following configuration:

   **Option A: Using Python directly (simpler)**
   ```json
   {
     "mcpServers": {
       "tradingview": {
         "command": "python",
         "args": [
           "C:\\Users\\YOUR_USERNAME\\tradingview-mcp-server\\server.py"
         ]
       }
     }
   }
   ```

   **Option B: Using virtual environment (recommended)**
   ```json
   {
     "mcpServers": {
       "tradingview": {
         "command": "C:\\Users\\YOUR_USERNAME\\tradingview-mcp-server\\venv\\Scripts\\python.exe",
         "args": [
           "C:\\Users\\YOUR_USERNAME\\tradingview-mcp-server\\server.py"
         ]
       }
     }
   }
   ```

   Replace `YOUR_USERNAME` with your actual Windows username.

3. Save the file and restart Claude Desktop.

### Step 4: Verify Installation

1. Open Claude Desktop
2. Look for the MCP tools icon (hammer icon) in the interface
3. You should see the TradingView tools listed

## Available Tools

### 1. get_technical_analysis
Get comprehensive technical analysis for any stock.

**Example prompts:**
- "Get technical analysis for AAPL"
- "Analyze TSLA on the 4-hour timeframe"
- "What's the technical outlook for MSFT?"

### 2. get_quote
Get real-time price quotes.

**Example prompts:**
- "What's the current price of NVDA?"
- "Get me a quote for AMD"

### 3. search_symbols
Search for any tradable symbol.

**Example prompts:**
- "Search for Apple stock"
- "Find Bitcoin trading pairs"
- "Search for EURUSD forex"

### 4. get_market_overview
Get an overview of major market indices.

**Example prompts:**
- "How is the US market doing today?"
- "Give me a crypto market overview"
- "Show forex market overview"

### 5. get_screener
Find stocks based on criteria.

**Example prompts:**
- "Show me top gainers today"
- "What are the most active stocks?"
- "Find oversold stocks"
- "Show top losers"

### 6. get_crypto_analysis
Technical analysis for cryptocurrencies.

**Example prompts:**
- "Analyze Bitcoin"
- "Get Ethereum technical analysis on the 1-hour chart"
- "What's the outlook for SOL?"

### 7. get_forex_analysis
Forex pair analysis with pivot points.

**Example prompts:**
- "Analyze EURUSD"
- "Get GBPUSD technical analysis"
- "What are the pivot points for USDJPY?"

## Supported Exchanges

- **US Stocks**: NASDAQ, NYSE, AMEX
- **Crypto**: BINANCE, COINBASE, KRAKEN, BITSTAMP
- **Forex**: FX_IDC (Forex market)
- **International**: NSE (India), BSE (India), LSE (UK), TSX (Canada), ASX (Australia)

## Time Intervals

- `1m` - 1 minute
- `5m` - 5 minutes
- `15m` - 15 minutes
- `30m` - 30 minutes
- `1h` - 1 hour
- `2h` - 2 hours
- `4h` - 4 hours
- `1d` - 1 day (default)
- `1w` - 1 week
- `1M` - 1 month

## Troubleshooting

### "Python not found" error
- Make sure Python is added to your PATH
- Try using the full path to Python: `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python311\python.exe`

### MCP server not connecting
1. Check the Claude Desktop logs at `%APPDATA%\Claude\logs`
2. Verify the path in `claude_desktop_config.json` is correct
3. Make sure all dependencies are installed
4. Try running the server manually to check for errors:
   ```cmd
   python C:\Users\YOUR_USERNAME\tradingview-mcp-server\server.py
   ```

### Import errors
- Reinstall dependencies:
  ```cmd
  pip install --upgrade mcp tradingview-ta requests
  ```

### "No module named 'mcp'" error
- Install the MCP package:
  ```cmd
  pip install mcp
  ```

## Data Disclaimer

This MCP server uses the TradingView Technical Analysis library which provides data from TradingView. The data is for informational purposes only and should not be considered as financial advice. Always do your own research before making investment decisions.

## License

MIT License

## Contributing

Feel free to submit issues and pull requests to improve this MCP server.
