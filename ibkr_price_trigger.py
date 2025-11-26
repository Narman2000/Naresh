#!/usr/bin/env python3
"""
IBKR Price Trigger Trading Script
Monitors a stock price and executes a buy order when the target price is touched.
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time


class IBKRTradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.next_order_id = None
        self.current_price = None
        self.target_price_touched = False
        self.connected = False

    def nextValidId(self, orderId: int):
        """Receives the next valid order ID"""
        super().nextValidId(orderId)
        self.next_order_id = orderId
        self.connected = True
        print(f"Next valid order ID: {orderId}")

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        """Handle error messages"""
        print(f"Error {errorCode}: {errorString}")

    def tickPrice(self, reqId, tickType, price, attrib):
        """Receives real-time price updates"""
        # tickType 4 = LAST price, 1 = BID, 2 = ASK
        if tickType in [1, 2, 4]:  # Using BID, ASK, or LAST
            self.current_price = price
            print(f"Current price: ${price:.2f}")

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice,
                   permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        """Receives order status updates"""
        print(f"Order {orderId} - Status: {status}, Filled: {filled}, "
              f"Remaining: {remaining}, Avg Fill Price: {avgFillPrice}")

    def openOrder(self, orderId, contract, order, orderState):
        """Receives open order information"""
        print(f"Open Order - ID: {orderId}, Symbol: {contract.symbol}, "
              f"Action: {order.action}, Quantity: {order.totalQuantity}")

    def execDetails(self, reqId, contract, execution):
        """Receives execution details"""
        print(f"Execution - Symbol: {contract.symbol}, Shares: {execution.shares}, "
              f"Price: ${execution.price:.2f}, Time: {execution.time}")


def create_stock_contract(symbol, exchange="SMART", currency="USD"):
    """Create a stock contract"""
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = exchange
    contract.currency = currency
    return contract


def create_market_order(action, quantity):
    """Create a market order"""
    order = Order()
    order.action = action  # "BUY" or "SELL"
    order.totalQuantity = quantity
    order.orderType = "MKT"
    return order


def create_limit_order(action, quantity, limit_price):
    """Create a limit order"""
    order = Order()
    order.action = action  # "BUY" or "SELL"
    order.totalQuantity = quantity
    order.orderType = "LMT"
    order.lmtPrice = limit_price
    return order


def monitor_and_trade(app, symbol, target_price, quantity,
                      order_type="MARKET", limit_price=None,
                      price_condition="BELOW"):
    """
    Monitor stock price and execute trade when target is reached

    Args:
        app: IBKRTradingApp instance
        symbol: Stock symbol to monitor
        target_price: Price threshold to trigger the order
        quantity: Number of shares to buy
        order_type: "MARKET" or "LIMIT"
        limit_price: Price for limit order (only if order_type is "LIMIT")
        price_condition: "BELOW" or "ABOVE" - trigger when price goes below/above target
    """
    # Create contract
    contract = create_stock_contract(symbol)

    # Request market data
    app.reqMarketDataType(1)  # 1 = Live data, 3 = Delayed data
    app.reqMktData(1, contract, "", False, False, [])

    print(f"\n{'='*60}")
    print(f"Monitoring {symbol}")
    print(f"Target Price: ${target_price:.2f}")
    print(f"Condition: Price goes {price_condition} target")
    print(f"Order Type: {order_type}")
    print(f"Quantity: {quantity} shares")
    print(f"{'='*60}\n")

    # Wait for price updates and check condition
    while not app.target_price_touched:
        if app.current_price is not None:
            # Check if target price condition is met
            if price_condition == "BELOW" and app.current_price <= target_price:
                print(f"\n🎯 Target price touched! Current: ${app.current_price:.2f}")
                app.target_price_touched = True
                break
            elif price_condition == "ABOVE" and app.current_price >= target_price:
                print(f"\n🎯 Target price touched! Current: ${app.current_price:.2f}")
                app.target_price_touched = True
                break
        time.sleep(1)

    # Cancel market data
    app.cancelMktData(1)

    # Wait for next valid order ID
    while app.next_order_id is None:
        time.sleep(0.1)

    # Place the order
    print(f"\n📈 Placing BUY order for {quantity} shares of {symbol}...")

    if order_type == "MARKET":
        order = create_market_order("BUY", quantity)
    else:  # LIMIT
        if limit_price is None:
            limit_price = app.current_price
        order = create_limit_order("BUY", quantity, limit_price)

    app.placeOrder(app.next_order_id, contract, order)
    print(f"✅ Order submitted with ID: {app.next_order_id}")

    # Keep connection alive to receive order updates
    time.sleep(5)


def main():
    """Main function to run the trading bot"""
    # Configuration
    SYMBOL = "AAPL"           # Stock symbol to trade
    TARGET_PRICE = 150.00     # Price threshold
    QUANTITY = 10             # Number of shares to buy
    ORDER_TYPE = "MARKET"     # "MARKET" or "LIMIT"
    LIMIT_PRICE = None        # Only used if ORDER_TYPE is "LIMIT"
    PRICE_CONDITION = "BELOW" # "BELOW" or "ABOVE"

    # IBKR Gateway settings
    HOST = "127.0.0.1"
    PORT = 4002              # Gateway port (use 7497 for TWS paper trading)
    CLIENT_ID = 1

    # Create app instance
    app = IBKRTradingApp()

    # Connect to IBKR Gateway
    print(f"Connecting to IBKR Gateway at {HOST}:{PORT}...")
    app.connect(HOST, PORT, CLIENT_ID)

    # Start the socket in a separate thread
    api_thread = threading.Thread(target=app.run, daemon=True)
    api_thread.start()

    # Wait for connection and next valid order ID
    timeout = 10
    start_time = time.time()
    while not app.connected and (time.time() - start_time) < timeout:
        time.sleep(0.5)

    if app.connected and app.isConnected():
        print("✅ Connected to IBKR Gateway")

        try:
            # Monitor and trade
            monitor_and_trade(
                app=app,
                symbol=SYMBOL,
                target_price=TARGET_PRICE,
                quantity=QUANTITY,
                order_type=ORDER_TYPE,
                limit_price=LIMIT_PRICE,
                price_condition=PRICE_CONDITION
            )
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        finally:
            # Disconnect
            print("\nDisconnecting...")
            app.disconnect()
    else:
        print("❌ Failed to connect to IBKR Gateway")


if __name__ == "__main__":
    main()
