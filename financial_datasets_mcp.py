#!/usr/bin/env python3
"""
Financial Datasets MCP Server for Claude AI Desktop

This MCP server provides tools for accessing financial market data including:
- Real-time and historical stock prices
- Company information and fundamentals
- Financial statements (income, balance sheet, cash flow)
- Market news and analysis
- Stock screening and filtering

Author: Generated for Claude AI Desktop integration
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Initialize MCP Server
server = Server("financial-datasets")

# API Configuration
# Supports multiple data providers - set your preferred API key
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "demo")
FINANCIAL_DATASETS_API_KEY = os.environ.get("FINANCIAL_DATASETS_API_KEY", "")
FMP_API_KEY = os.environ.get("FMP_API_KEY", "")  # Financial Modeling Prep

# Base URLs
ALPHA_VANTAGE_BASE = "https://www.alphavantage.co/query"
FMP_BASE = "https://financialmodelingprep.com/api/v3"
FINANCIAL_DATASETS_BASE = "https://api.financialdatasets.ai"


async def fetch_json(url: str, params: dict = None) -> dict:
    """Fetch JSON data from URL with error handling."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}"}
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response"}


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available financial data tools."""
    return [
        types.Tool(
            name="get_stock_quote",
            description="Get the current stock quote including price, volume, and daily change for a given ticker symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_company_overview",
            description="Get comprehensive company information including description, sector, industry, market cap, PE ratio, and other fundamentals",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_historical_prices",
            description="Get historical daily stock prices (open, high, low, close, volume) for a given period",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days of historical data (default: 30, max: 365)",
                        "default": 30
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_income_statement",
            description="Get the income statement (revenue, expenses, profit) for a company - annual or quarterly",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["annual", "quarterly"],
                        "description": "Report period type",
                        "default": "annual"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_balance_sheet",
            description="Get the balance sheet (assets, liabilities, equity) for a company - annual or quarterly",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["annual", "quarterly"],
                        "description": "Report period type",
                        "default": "annual"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_cash_flow",
            description="Get the cash flow statement (operating, investing, financing activities) for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["annual", "quarterly"],
                        "description": "Report period type",
                        "default": "annual"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_market_news",
            description="Get latest market news and sentiment for a specific stock or general market news",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (optional, leave empty for general market news)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of news articles to return (default: 10, max: 50)",
                        "default": 10
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_technical_indicators",
            description="Get technical analysis indicators (SMA, EMA, RSI, MACD) for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                    },
                    "indicator": {
                        "type": "string",
                        "enum": ["SMA", "EMA", "RSI", "MACD", "BBANDS"],
                        "description": "Technical indicator type"
                    },
                    "interval": {
                        "type": "string",
                        "enum": ["daily", "weekly", "monthly"],
                        "description": "Time interval",
                        "default": "daily"
                    },
                    "time_period": {
                        "type": "integer",
                        "description": "Number of periods for the indicator (e.g., 14 for RSI, 20 for SMA)",
                        "default": 14
                    }
                },
                "required": ["symbol", "indicator"]
            }
        ),
        types.Tool(
            name="get_earnings_calendar",
            description="Get upcoming earnings announcements for a specific stock or the broader market",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (optional)"
                    },
                    "days_ahead": {
                        "type": "integer",
                        "description": "Number of days to look ahead (default: 7, max: 30)",
                        "default": 7
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="screen_stocks",
            description="Screen stocks based on financial criteria (market cap, PE ratio, dividend yield, sector)",
            inputSchema={
                "type": "object",
                "properties": {
                    "min_market_cap": {
                        "type": "number",
                        "description": "Minimum market capitalization in billions USD"
                    },
                    "max_market_cap": {
                        "type": "number",
                        "description": "Maximum market capitalization in billions USD"
                    },
                    "min_pe": {
                        "type": "number",
                        "description": "Minimum Price-to-Earnings ratio"
                    },
                    "max_pe": {
                        "type": "number",
                        "description": "Maximum Price-to-Earnings ratio"
                    },
                    "min_dividend_yield": {
                        "type": "number",
                        "description": "Minimum dividend yield percentage"
                    },
                    "sector": {
                        "type": "string",
                        "description": "Filter by sector (e.g., Technology, Healthcare, Finance)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 20)",
                        "default": 20
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="compare_stocks",
            description="Compare key metrics between multiple stocks side by side",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of stock ticker symbols to compare (2-5 symbols)"
                    }
                },
                "required": ["symbols"]
            }
        ),
        types.Tool(
            name="get_forex_rate",
            description="Get current exchange rate between two currencies",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "Source currency code (e.g., USD, EUR, GBP)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Target currency code (e.g., USD, EUR, GBP)"
                    }
                },
                "required": ["from_currency", "to_currency"]
            }
        ),
        types.Tool(
            name="get_crypto_price",
            description="Get current cryptocurrency price and market data",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Cryptocurrency symbol (e.g., BTC, ETH, SOL)"
                    },
                    "market": {
                        "type": "string",
                        "description": "Market currency (default: USD)",
                        "default": "USD"
                    }
                },
                "required": ["symbol"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls for financial data retrieval."""

    try:
        if name == "get_stock_quote":
            result = await get_stock_quote(arguments["symbol"])
        elif name == "get_company_overview":
            result = await get_company_overview(arguments["symbol"])
        elif name == "get_historical_prices":
            result = await get_historical_prices(
                arguments["symbol"],
                arguments.get("days", 30)
            )
        elif name == "get_income_statement":
            result = await get_income_statement(
                arguments["symbol"],
                arguments.get("period", "annual")
            )
        elif name == "get_balance_sheet":
            result = await get_balance_sheet(
                arguments["symbol"],
                arguments.get("period", "annual")
            )
        elif name == "get_cash_flow":
            result = await get_cash_flow(
                arguments["symbol"],
                arguments.get("period", "annual")
            )
        elif name == "get_market_news":
            result = await get_market_news(
                arguments.get("symbol"),
                arguments.get("limit", 10)
            )
        elif name == "get_technical_indicators":
            result = await get_technical_indicators(
                arguments["symbol"],
                arguments["indicator"],
                arguments.get("interval", "daily"),
                arguments.get("time_period", 14)
            )
        elif name == "get_earnings_calendar":
            result = await get_earnings_calendar(
                arguments.get("symbol"),
                arguments.get("days_ahead", 7)
            )
        elif name == "screen_stocks":
            result = await screen_stocks(arguments)
        elif name == "compare_stocks":
            result = await compare_stocks(arguments["symbols"])
        elif name == "get_forex_rate":
            result = await get_forex_rate(
                arguments["from_currency"],
                arguments["to_currency"]
            )
        elif name == "get_crypto_price":
            result = await get_crypto_price(
                arguments["symbol"],
                arguments.get("market", "USD")
            )
        else:
            result = {"error": f"Unknown tool: {name}"}

        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str)
        )]

    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


# Tool Implementation Functions

async def get_stock_quote(symbol: str) -> dict:
    """Get current stock quote from Alpha Vantage."""
    symbol = symbol.upper().strip()

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    quote = data.get("Global Quote", {})

    if not quote:
        return {"error": f"No quote data found for symbol: {symbol}"}

    return {
        "symbol": quote.get("01. symbol", symbol),
        "price": float(quote.get("05. price", 0)),
        "open": float(quote.get("02. open", 0)),
        "high": float(quote.get("03. high", 0)),
        "low": float(quote.get("04. low", 0)),
        "volume": int(quote.get("06. volume", 0)),
        "previous_close": float(quote.get("08. previous close", 0)),
        "change": float(quote.get("09. change", 0)),
        "change_percent": quote.get("10. change percent", "0%"),
        "latest_trading_day": quote.get("07. latest trading day"),
        "timestamp": datetime.now().isoformat()
    }


async def get_company_overview(symbol: str) -> dict:
    """Get company overview and fundamentals from Alpha Vantage."""
    symbol = symbol.upper().strip()

    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    if not data or "Symbol" not in data:
        return {"error": f"No company data found for symbol: {symbol}"}

    return {
        "symbol": data.get("Symbol"),
        "name": data.get("Name"),
        "description": data.get("Description"),
        "exchange": data.get("Exchange"),
        "currency": data.get("Currency"),
        "country": data.get("Country"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": data.get("MarketCapitalization"),
        "pe_ratio": data.get("PERatio"),
        "peg_ratio": data.get("PEGRatio"),
        "book_value": data.get("BookValue"),
        "dividend_per_share": data.get("DividendPerShare"),
        "dividend_yield": data.get("DividendYield"),
        "eps": data.get("EPS"),
        "revenue_per_share_ttm": data.get("RevenuePerShareTTM"),
        "profit_margin": data.get("ProfitMargin"),
        "operating_margin_ttm": data.get("OperatingMarginTTM"),
        "return_on_assets_ttm": data.get("ReturnOnAssetsTTM"),
        "return_on_equity_ttm": data.get("ReturnOnEquityTTM"),
        "revenue_ttm": data.get("RevenueTTM"),
        "gross_profit_ttm": data.get("GrossProfitTTM"),
        "52_week_high": data.get("52WeekHigh"),
        "52_week_low": data.get("52WeekLow"),
        "50_day_moving_average": data.get("50DayMovingAverage"),
        "200_day_moving_average": data.get("200DayMovingAverage"),
        "shares_outstanding": data.get("SharesOutstanding"),
        "beta": data.get("Beta"),
        "forward_pe": data.get("ForwardPE"),
        "analyst_target_price": data.get("AnalystTargetPrice"),
        "timestamp": datetime.now().isoformat()
    }


async def get_historical_prices(symbol: str, days: int = 30) -> dict:
    """Get historical daily prices from Alpha Vantage."""
    symbol = symbol.upper().strip()
    days = min(max(days, 1), 365)

    # Use compact for <= 100 days, full for more
    outputsize = "compact" if days <= 100 else "full"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    time_series = data.get("Time Series (Daily)", {})

    if not time_series:
        return {"error": f"No historical data found for symbol: {symbol}"}

    # Sort by date and limit to requested days
    sorted_dates = sorted(time_series.keys(), reverse=True)[:days]

    prices = []
    for date in sorted_dates:
        day_data = time_series[date]
        prices.append({
            "date": date,
            "open": float(day_data.get("1. open", 0)),
            "high": float(day_data.get("2. high", 0)),
            "low": float(day_data.get("3. low", 0)),
            "close": float(day_data.get("4. close", 0)),
            "volume": int(day_data.get("5. volume", 0))
        })

    return {
        "symbol": symbol,
        "days_requested": days,
        "days_returned": len(prices),
        "prices": prices,
        "timestamp": datetime.now().isoformat()
    }


async def get_income_statement(symbol: str, period: str = "annual") -> dict:
    """Get income statement data from Alpha Vantage."""
    symbol = symbol.upper().strip()

    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    reports_key = "annualReports" if period == "annual" else "quarterlyReports"
    reports = data.get(reports_key, [])

    if not reports:
        return {"error": f"No income statement data found for symbol: {symbol}"}

    # Return the most recent 4 reports
    formatted_reports = []
    for report in reports[:4]:
        formatted_reports.append({
            "fiscal_date_ending": report.get("fiscalDateEnding"),
            "reported_currency": report.get("reportedCurrency"),
            "total_revenue": report.get("totalRevenue"),
            "gross_profit": report.get("grossProfit"),
            "operating_income": report.get("operatingIncome"),
            "net_income": report.get("netIncome"),
            "ebitda": report.get("ebitda"),
            "cost_of_revenue": report.get("costOfRevenue"),
            "operating_expenses": report.get("operatingExpenses"),
            "research_and_development": report.get("researchAndDevelopment"),
            "interest_expense": report.get("interestExpense"),
            "income_tax_expense": report.get("incomeTaxExpense"),
            "eps": report.get("reportedEPS")
        })

    return {
        "symbol": symbol,
        "period": period,
        "reports": formatted_reports,
        "timestamp": datetime.now().isoformat()
    }


async def get_balance_sheet(symbol: str, period: str = "annual") -> dict:
    """Get balance sheet data from Alpha Vantage."""
    symbol = symbol.upper().strip()

    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    reports_key = "annualReports" if period == "annual" else "quarterlyReports"
    reports = data.get(reports_key, [])

    if not reports:
        return {"error": f"No balance sheet data found for symbol: {symbol}"}

    formatted_reports = []
    for report in reports[:4]:
        formatted_reports.append({
            "fiscal_date_ending": report.get("fiscalDateEnding"),
            "reported_currency": report.get("reportedCurrency"),
            "total_assets": report.get("totalAssets"),
            "total_liabilities": report.get("totalLiabilities"),
            "total_shareholder_equity": report.get("totalShareholderEquity"),
            "cash_and_equivalents": report.get("cashAndCashEquivalentsAtCarryingValue"),
            "short_term_investments": report.get("shortTermInvestments"),
            "total_current_assets": report.get("totalCurrentAssets"),
            "total_current_liabilities": report.get("totalCurrentLiabilities"),
            "long_term_debt": report.get("longTermDebt"),
            "short_term_debt": report.get("shortTermDebt"),
            "retained_earnings": report.get("retainedEarnings"),
            "common_stock": report.get("commonStock"),
            "treasury_stock": report.get("treasuryStock"),
            "inventory": report.get("inventory"),
            "accounts_receivable": report.get("currentNetReceivables"),
            "accounts_payable": report.get("currentAccountsPayable")
        })

    return {
        "symbol": symbol,
        "period": period,
        "reports": formatted_reports,
        "timestamp": datetime.now().isoformat()
    }


async def get_cash_flow(symbol: str, period: str = "annual") -> dict:
    """Get cash flow statement from Alpha Vantage."""
    symbol = symbol.upper().strip()

    params = {
        "function": "CASH_FLOW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    reports_key = "annualReports" if period == "annual" else "quarterlyReports"
    reports = data.get(reports_key, [])

    if not reports:
        return {"error": f"No cash flow data found for symbol: {symbol}"}

    formatted_reports = []
    for report in reports[:4]:
        formatted_reports.append({
            "fiscal_date_ending": report.get("fiscalDateEnding"),
            "reported_currency": report.get("reportedCurrency"),
            "operating_cashflow": report.get("operatingCashflow"),
            "cashflow_from_investment": report.get("cashflowFromInvestment"),
            "cashflow_from_financing": report.get("cashflowFromFinancing"),
            "net_income": report.get("netIncome"),
            "depreciation": report.get("depreciationDepletionAndAmortization"),
            "capital_expenditures": report.get("capitalExpenditures"),
            "dividend_payout": report.get("dividendPayout"),
            "stock_repurchase": report.get("paymentsForRepurchaseOfCommonStock"),
            "proceeds_from_stock_issuance": report.get("proceedsFromIssuanceOfCommonStock"),
            "change_in_cash": report.get("changeInCashAndCashEquivalents"),
            "free_cash_flow": None  # Calculated below
        })

        # Calculate free cash flow
        try:
            operating = float(report.get("operatingCashflow", 0) or 0)
            capex = float(report.get("capitalExpenditures", 0) or 0)
            formatted_reports[-1]["free_cash_flow"] = operating - abs(capex)
        except (ValueError, TypeError):
            pass

    return {
        "symbol": symbol,
        "period": period,
        "reports": formatted_reports,
        "timestamp": datetime.now().isoformat()
    }


async def get_market_news(symbol: Optional[str] = None, limit: int = 10) -> dict:
    """Get market news from Alpha Vantage."""
    limit = min(max(limit, 1), 50)

    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": ALPHA_VANTAGE_API_KEY,
        "limit": limit
    }

    if symbol:
        params["tickers"] = symbol.upper().strip()

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    feed = data.get("feed", [])

    if not feed:
        return {"message": "No news articles found", "articles": []}

    articles = []
    for article in feed[:limit]:
        articles.append({
            "title": article.get("title"),
            "url": article.get("url"),
            "source": article.get("source"),
            "summary": article.get("summary"),
            "published": article.get("time_published"),
            "overall_sentiment": article.get("overall_sentiment_label"),
            "sentiment_score": article.get("overall_sentiment_score"),
            "ticker_sentiment": [
                {
                    "ticker": ts.get("ticker"),
                    "relevance_score": ts.get("relevance_score"),
                    "sentiment": ts.get("ticker_sentiment_label"),
                    "sentiment_score": ts.get("ticker_sentiment_score")
                }
                for ts in article.get("ticker_sentiment", [])
            ]
        })

    return {
        "symbol": symbol,
        "total_articles": len(articles),
        "articles": articles,
        "timestamp": datetime.now().isoformat()
    }


async def get_technical_indicators(
    symbol: str,
    indicator: str,
    interval: str = "daily",
    time_period: int = 14
) -> dict:
    """Get technical indicators from Alpha Vantage."""
    symbol = symbol.upper().strip()
    indicator = indicator.upper()

    # Map intervals
    interval_map = {
        "daily": "daily",
        "weekly": "weekly",
        "monthly": "monthly"
    }
    av_interval = interval_map.get(interval, "daily")

    params = {
        "function": indicator,
        "symbol": symbol,
        "interval": av_interval,
        "time_period": time_period,
        "series_type": "close",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    # Find the technical analysis key in response
    ta_key = None
    for key in data.keys():
        if "Technical Analysis" in key:
            ta_key = key
            break

    if not ta_key:
        return {"error": f"No technical indicator data found for {indicator}"}

    ta_data = data.get(ta_key, {})

    # Get the most recent 20 data points
    sorted_dates = sorted(ta_data.keys(), reverse=True)[:20]

    values = []
    for date in sorted_dates:
        day_data = ta_data[date]
        values.append({
            "date": date,
            **{k: float(v) for k, v in day_data.items()}
        })

    return {
        "symbol": symbol,
        "indicator": indicator,
        "interval": interval,
        "time_period": time_period,
        "values": values,
        "timestamp": datetime.now().isoformat()
    }


async def get_earnings_calendar(
    symbol: Optional[str] = None,
    days_ahead: int = 7
) -> dict:
    """Get earnings calendar from Alpha Vantage."""
    days_ahead = min(max(days_ahead, 1), 30)

    params = {
        "function": "EARNINGS_CALENDAR",
        "horizon": f"{days_ahead}day" if days_ahead <= 3 else "3month",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    if symbol:
        params["symbol"] = symbol.upper().strip()

    # Alpha Vantage returns CSV for this endpoint
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(ALPHA_VANTAGE_BASE, params=params)
            response.raise_for_status()
            csv_data = response.text
        except Exception as e:
            return {"error": f"Failed to fetch earnings calendar: {str(e)}"}

    # Parse CSV
    lines = csv_data.strip().split("\n")
    if len(lines) < 2:
        return {"message": "No upcoming earnings found", "earnings": []}

    headers = lines[0].split(",")
    earnings = []

    today = datetime.now().date()
    cutoff = today + timedelta(days=days_ahead)

    for line in lines[1:]:
        values = line.split(",")
        if len(values) >= len(headers):
            record = dict(zip(headers, values))

            # Filter by date
            try:
                report_date = datetime.strptime(
                    record.get("reportDate", ""),
                    "%Y-%m-%d"
                ).date()
                if report_date > cutoff:
                    continue
            except ValueError:
                continue

            earnings.append({
                "symbol": record.get("symbol"),
                "name": record.get("name"),
                "report_date": record.get("reportDate"),
                "fiscal_date_ending": record.get("fiscalDateEnding"),
                "estimate": record.get("estimate"),
                "currency": record.get("currency")
            })

    return {
        "symbol": symbol,
        "days_ahead": days_ahead,
        "total_earnings": len(earnings),
        "earnings": earnings[:50],  # Limit results
        "timestamp": datetime.now().isoformat()
    }


async def screen_stocks(criteria: dict) -> dict:
    """Screen stocks based on criteria using Alpha Vantage."""
    # Note: Alpha Vantage doesn't have a native screener
    # This provides a simulated screener based on common criteria

    # For a real implementation, you would:
    # 1. Use a database of stocks with pre-fetched fundamentals
    # 2. Or use a different API with screening capabilities

    return {
        "message": "Stock screening requires a premium data provider or local database",
        "criteria_received": criteria,
        "suggestion": "Consider using Financial Modeling Prep API or maintaining a local database of stock fundamentals for screening. Set FMP_API_KEY environment variable for screening functionality.",
        "timestamp": datetime.now().isoformat()
    }


async def compare_stocks(symbols: list) -> dict:
    """Compare multiple stocks side by side."""
    if len(symbols) < 2:
        return {"error": "Please provide at least 2 symbols to compare"}
    if len(symbols) > 5:
        return {"error": "Maximum 5 symbols allowed for comparison"}

    comparisons = []

    for symbol in symbols:
        # Get quote and overview for each symbol
        quote = await get_stock_quote(symbol)
        overview = await get_company_overview(symbol)

        comparisons.append({
            "symbol": symbol.upper(),
            "name": overview.get("name", "N/A"),
            "sector": overview.get("sector", "N/A"),
            "price": quote.get("price", "N/A"),
            "change_percent": quote.get("change_percent", "N/A"),
            "market_cap": overview.get("market_cap", "N/A"),
            "pe_ratio": overview.get("pe_ratio", "N/A"),
            "eps": overview.get("eps", "N/A"),
            "dividend_yield": overview.get("dividend_yield", "N/A"),
            "52_week_high": overview.get("52_week_high", "N/A"),
            "52_week_low": overview.get("52_week_low", "N/A"),
            "beta": overview.get("beta", "N/A"),
            "profit_margin": overview.get("profit_margin", "N/A")
        })

    return {
        "comparison": comparisons,
        "symbols_compared": len(comparisons),
        "timestamp": datetime.now().isoformat()
    }


async def get_forex_rate(from_currency: str, to_currency: str) -> dict:
    """Get forex exchange rate from Alpha Vantage."""
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency,
        "to_currency": to_currency,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    rate_data = data.get("Realtime Currency Exchange Rate", {})

    if not rate_data:
        return {"error": f"No exchange rate found for {from_currency}/{to_currency}"}

    return {
        "from_currency": rate_data.get("1. From_Currency Code"),
        "from_currency_name": rate_data.get("2. From_Currency Name"),
        "to_currency": rate_data.get("3. To_Currency Code"),
        "to_currency_name": rate_data.get("4. To_Currency Name"),
        "exchange_rate": float(rate_data.get("5. Exchange Rate", 0)),
        "last_refreshed": rate_data.get("6. Last Refreshed"),
        "timezone": rate_data.get("7. Time Zone"),
        "bid_price": rate_data.get("8. Bid Price"),
        "ask_price": rate_data.get("9. Ask Price"),
        "timestamp": datetime.now().isoformat()
    }


async def get_crypto_price(symbol: str, market: str = "USD") -> dict:
    """Get cryptocurrency price from Alpha Vantage."""
    symbol = symbol.upper().strip()
    market = market.upper().strip()

    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": symbol,
        "to_currency": market,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    data = await fetch_json(ALPHA_VANTAGE_BASE, params)

    if "error" in data:
        return data

    rate_data = data.get("Realtime Currency Exchange Rate", {})

    if not rate_data:
        return {"error": f"No price found for {symbol}/{market}"}

    return {
        "symbol": symbol,
        "name": rate_data.get("2. From_Currency Name"),
        "market": market,
        "price": float(rate_data.get("5. Exchange Rate", 0)),
        "last_refreshed": rate_data.get("6. Last Refreshed"),
        "bid_price": rate_data.get("8. Bid Price"),
        "ask_price": rate_data.get("9. Ask Price"),
        "timestamp": datetime.now().isoformat()
    }


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available data resources."""
    return [
        types.Resource(
            uri="financial://market/overview",
            name="Market Overview",
            description="Current market overview including major indices status",
            mimeType="application/json"
        ),
        types.Resource(
            uri="financial://sectors/performance",
            name="Sector Performance",
            description="Performance of major market sectors",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    if uri == "financial://market/overview":
        # Get major indices
        indices = ["SPY", "QQQ", "DIA", "IWM"]
        overview = []
        for idx in indices:
            quote = await get_stock_quote(idx)
            overview.append({
                "index": idx,
                "price": quote.get("price"),
                "change_percent": quote.get("change_percent")
            })
        return json.dumps({
            "market_overview": overview,
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    elif uri == "financial://sectors/performance":
        # Major sector ETFs
        sectors = {
            "XLK": "Technology",
            "XLF": "Financials",
            "XLV": "Healthcare",
            "XLE": "Energy",
            "XLY": "Consumer Discretionary",
            "XLP": "Consumer Staples",
            "XLI": "Industrials",
            "XLB": "Materials",
            "XLU": "Utilities",
            "XLRE": "Real Estate"
        }
        performance = []
        for etf, sector in sectors.items():
            quote = await get_stock_quote(etf)
            performance.append({
                "sector": sector,
                "etf": etf,
                "change_percent": quote.get("change_percent")
            })
        return json.dumps({
            "sector_performance": performance,
            "timestamp": datetime.now().isoformat()
        }, indent=2)

    return json.dumps({"error": f"Unknown resource: {uri}"})


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
