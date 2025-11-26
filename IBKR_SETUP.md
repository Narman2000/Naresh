# IBKR Price Trigger Trading Setup

## Prerequisites

1. **Interactive Brokers Account**
   - Active IBKR account (paper or live)
   - IB Gateway or TWS installed

2. **Python Environment**
   - Python 3.7 or higher
   - pip package manager

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install ibapi
```

### Step 2: Configure IB Gateway

1. **Start IB Gateway**
   - Open IB Gateway application
   - Log in with your credentials

2. **Configure API Settings**
   - Go to Configure → Settings → API → Settings
   - Enable "Enable ActiveX and Socket Clients"
   - Add "127.0.0.1" to "Trusted IP Addresses"
   - **Socket port**: 4002 (live) or 4001 (paper trading)
   - Enable "Read-Only API" if you want to test without placing real orders
   - Disable "Read-Only API" to allow order placement
   - Click "OK" to save

3. **Important Settings**
   - Uncheck "Read-Only API" to allow trading
   - Check "Download open orders on connection" (recommended)
   - Set "Master API client ID" if needed

## Usage

### Basic Configuration

Edit the `main()` function in `ibkr_price_trigger.py`:

```python
SYMBOL = "AAPL"           # Stock symbol to monitor
TARGET_PRICE = 150.00     # Price threshold to trigger order
QUANTITY = 10             # Number of shares to buy
ORDER_TYPE = "MARKET"     # "MARKET" or "LIMIT"
LIMIT_PRICE = None        # Set price if using LIMIT order
PRICE_CONDITION = "BELOW" # "BELOW" or "ABOVE"
```

### Running the Script

```bash
python ibkr_price_trigger.py
```

### Examples

#### Example 1: Buy when price drops below $150
```python
SYMBOL = "AAPL"
TARGET_PRICE = 150.00
QUANTITY = 10
ORDER_TYPE = "MARKET"
PRICE_CONDITION = "BELOW"
```

#### Example 2: Buy when price rises above $200
```python
SYMBOL = "TSLA"
TARGET_PRICE = 200.00
QUANTITY = 5
ORDER_TYPE = "MARKET"
PRICE_CONDITION = "ABOVE"
```

#### Example 3: Use limit order at specific price
```python
SYMBOL = "MSFT"
TARGET_PRICE = 350.00
QUANTITY = 20
ORDER_TYPE = "LIMIT"
LIMIT_PRICE = 351.00  # Buy at max $351
PRICE_CONDITION = "BELOW"
```

## Port Configuration

- **Port 4002**: IB Gateway Live Trading
- **Port 4001**: IB Gateway Paper Trading
- **Port 7497**: TWS Paper Trading
- **Port 7496**: TWS Live Trading

Change the PORT in the script according to your setup.

## Troubleshooting

### Connection Issues

1. **"Failed to connect" Error**
   - Ensure IB Gateway is running
   - Check the port number matches your Gateway settings
   - Verify 127.0.0.1 is in Trusted IP Addresses

2. **"Error 502: Couldn't connect to TWS"**
   - IB Gateway/TWS is not running
   - Wrong port number
   - API settings not enabled

3. **"Error 504: Not connected"**
   - Connection was lost
   - Restart IB Gateway and the script

### Trading Issues

1. **"Error 200: No security definition found"**
   - Invalid stock symbol
   - Check symbol format (use uppercase)

2. **Orders not executing**
   - Check if "Read-Only API" is disabled
   - Verify you have sufficient buying power
   - Check market hours (9:30 AM - 4:00 PM ET for US stocks)

3. **Market Data Issues**
   - May need market data subscription for real-time data
   - Use `app.reqMarketDataType(3)` for delayed data (free)
   - Use `app.reqMarketDataType(1)` for live data (requires subscription)

## Safety Tips

1. **Start with Paper Trading**
   - Test thoroughly with paper trading account first
   - Use port 4001 for paper trading

2. **Set Reasonable Limits**
   - Start with small quantities
   - Use limit orders to control execution price

3. **Monitor the Bot**
   - Don't leave unattended initially
   - Check logs and order confirmations

4. **Risk Management**
   - Set stop losses separately
   - Don't risk more than you can afford to lose
   - Consider market volatility

## Advanced Features

### Adding Stop Loss

Modify the script to add a stop loss after buying:

```python
def create_stop_loss_order(action, quantity, stop_price):
    order = Order()
    order.action = action  # "SELL" for stop loss
    order.totalQuantity = quantity
    order.orderType = "STP"
    order.auxPrice = stop_price
    return order
```

### Multiple Stock Monitoring

Create multiple app instances or use a loop to monitor multiple stocks.

## API Documentation

For more details, refer to:
- [IBKR API Documentation](https://interactivebrokers.github.io/tws-api/)
- [Python API Guide](https://interactivebrokers.github.io/tws-api/introduction.html)

## License

Use at your own risk. This is for educational purposes. Always test with paper trading first.
