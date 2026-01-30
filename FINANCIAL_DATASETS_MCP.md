# Financial Datasets MCP Server for Claude AI Desktop

A Model Context Protocol (MCP) server that provides comprehensive financial market data tools for Claude AI Desktop. This server enables Claude to access real-time stock quotes, company fundamentals, historical prices, financial statements, market news, and more.

## Features

### Available Tools

| Tool | Description |
|------|-------------|
| `get_stock_quote` | Get current stock price, volume, and daily change |
| `get_company_overview` | Get company information, sector, market cap, PE ratio, and fundamentals |
| `get_historical_prices` | Get historical daily OHLCV data (up to 365 days) |
| `get_income_statement` | Get income statement (annual or quarterly) |
| `get_balance_sheet` | Get balance sheet data (annual or quarterly) |
| `get_cash_flow` | Get cash flow statement (annual or quarterly) |
| `get_market_news` | Get latest market news with sentiment analysis |
| `get_technical_indicators` | Get technical indicators (SMA, EMA, RSI, MACD, BBANDS) |
| `get_earnings_calendar` | Get upcoming earnings announcements |
| `screen_stocks` | Screen stocks based on financial criteria |
| `compare_stocks` | Compare key metrics between multiple stocks |
| `get_forex_rate` | Get currency exchange rates |
| `get_crypto_price` | Get cryptocurrency prices |

### Available Resources

| Resource URI | Description |
|--------------|-------------|
| `financial://market/overview` | Current market overview with major indices |
| `financial://sectors/performance` | Performance of major market sectors |

## Installation

### Prerequisites

- Python 3.10 or higher
- Claude AI Desktop application

### Step 1: Install Dependencies

```bash
cd /path/to/Naresh
pip install -r requirements.txt
```

Or install MCP dependencies directly:

```bash
pip install mcp httpx
```

### Step 2: Get an API Key

This server uses [Alpha Vantage](https://www.alphavantage.co/) for financial data. Get a free API key:

1. Visit https://www.alphavantage.co/support/#api-key
2. Sign up for a free API key
3. The free tier allows 25 requests per day

### Step 3: Configure Claude Desktop

#### macOS

Edit the configuration file at:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Windows

Edit the configuration file at:
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### Linux

Edit the configuration file at:
```
~/.config/Claude/claude_desktop_config.json
```

### Step 4: Add Server Configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "financial-datasets": {
      "command": "python",
      "args": ["/full/path/to/Naresh/financial_datasets_mcp.py"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Important**: Replace `/full/path/to/Naresh/financial_datasets_mcp.py` with the actual absolute path to the script.

### Step 5: Restart Claude Desktop

After saving the configuration, restart Claude Desktop for the changes to take effect.

## Usage Examples

Once configured, you can ask Claude to use financial data tools naturally:

### Stock Quotes
```
"What's the current price of Apple stock?"
"Get me a quote for MSFT"
```

### Company Research
```
"Tell me about Tesla's fundamentals"
"What sector is Amazon in and what's their PE ratio?"
```

### Historical Data
```
"Show me the last 30 days of price history for GOOGL"
"What was NVDA's trading range over the past week?"
```

### Financial Statements
```
"Get Apple's latest income statement"
"Show me Microsoft's balance sheet"
"What's Amazon's free cash flow?"
```

### Market News
```
"What's the latest news about Tesla?"
"Get me market news with sentiment analysis"
```

### Technical Analysis
```
"Calculate the 14-day RSI for SPY"
"What's the 50-day moving average for AAPL?"
```

### Comparisons
```
"Compare Apple, Microsoft, and Google side by side"
"Which has a better PE ratio: AAPL or MSFT?"
```

### Forex & Crypto
```
"What's the EUR to USD exchange rate?"
"Get the current Bitcoin price"
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ALPHA_VANTAGE_API_KEY` | Your Alpha Vantage API key | Yes (or use "demo") |
| `FINANCIAL_DATASETS_API_KEY` | Financial Datasets API key (optional) | No |
| `FMP_API_KEY` | Financial Modeling Prep API key (optional) | No |

## API Rate Limits

### Alpha Vantage Free Tier
- 25 API requests per day
- 5 requests per minute

### Alpha Vantage Premium
- Higher rate limits available with paid plans
- Visit https://www.alphavantage.co/premium/ for details

## Troubleshooting

### Server Not Appearing in Claude

1. Verify the path in `claude_desktop_config.json` is absolute
2. Check that Python is in your system PATH
3. Ensure the configuration JSON is valid (use a JSON validator)
4. Check Claude Desktop logs for errors

### API Errors

1. Verify your API key is correct
2. Check if you've exceeded rate limits
3. The "demo" API key has limited functionality

### Import Errors

Ensure all dependencies are installed:
```bash
pip install mcp httpx
```

## Development

### Running Locally for Testing

```bash
export ALPHA_VANTAGE_API_KEY="your-key"
python financial_datasets_mcp.py
```

The server communicates via stdio, so it will wait for MCP protocol messages.

### Adding New Tools

To add a new tool:

1. Add the tool definition in `list_tools()`
2. Add the handler in `call_tool()`
3. Implement the async function

Example:
```python
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        # ... existing tools ...
        types.Tool(
            name="my_new_tool",
            description="Description of what this tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "Parameter description"}
                },
                "required": ["param1"]
            }
        )
    ]
```

## License

This project is provided as-is for use with Claude AI Desktop.

## Support

For issues with:
- **Claude Desktop**: Visit https://support.anthropic.com
- **Alpha Vantage API**: Visit https://www.alphavantage.co/support/
- **MCP Protocol**: Visit https://modelcontextprotocol.io/
