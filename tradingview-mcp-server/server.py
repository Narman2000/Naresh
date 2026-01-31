#!/usr/bin/env python3
"""
TradingView MCP Server for Claude AI Desktop
Provides real-time market data, technical analysis, and trading insights from TradingView.
"""

import asyncio
import json
import sys
from typing import Any, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
)

from tradingview_ta import TA_Handler, Interval, Exchange
import requests

# Initialize MCP Server
server = Server("tradingview-mcp-server")

# TradingView Interval mappings
INTERVAL_MAP = {
    "1m": Interval.INTERVAL_1_MINUTE,
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES,
    "30m": Interval.INTERVAL_30_MINUTES,
    "1h": Interval.INTERVAL_1_HOUR,
    "2h": Interval.INTERVAL_2_HOURS,
    "4h": Interval.INTERVAL_4_HOURS,
    "1d": Interval.INTERVAL_1_DAY,
    "1w": Interval.INTERVAL_1_WEEK,
    "1M": Interval.INTERVAL_1_MONTH,
}

# Common exchanges
EXCHANGE_MAP = {
    "NASDAQ": "NASDAQ",
    "NYSE": "NYSE",
    "AMEX": "AMEX",
    "BINANCE": "BINANCE",
    "COINBASE": "COINBASE",
    "KRAKEN": "KRAKEN",
    "FTX": "FTX",
    "BITSTAMP": "BITSTAMP",
    "FOREX": "FX_IDC",
    "CRYPTO": "BINANCE",
    "NSE": "NSE",
    "BSE": "BSE",
    "LSE": "LSE",
    "TSX": "TSX",
    "ASX": "ASX",
}


def get_technical_analysis(symbol: str, exchange: str = "NASDAQ", screener: str = "america", interval: str = "1d") -> dict:
    """Get technical analysis for a symbol from TradingView."""
    try:
        interval_enum = INTERVAL_MAP.get(interval, Interval.INTERVAL_1_DAY)

        handler = TA_Handler(
            symbol=symbol.upper(),
            screener=screener.lower(),
            exchange=exchange.upper(),
            interval=interval_enum
        )

        analysis = handler.get_analysis()

        return {
            "symbol": symbol.upper(),
            "exchange": exchange.upper(),
            "interval": interval,
            "time": datetime.now().isoformat(),
            "summary": {
                "recommendation": analysis.summary["RECOMMENDATION"],
                "buy_signals": analysis.summary["BUY"],
                "sell_signals": analysis.summary["SELL"],
                "neutral_signals": analysis.summary["NEUTRAL"],
            },
            "oscillators": {
                "recommendation": analysis.oscillators["RECOMMENDATION"],
                "buy": analysis.oscillators["BUY"],
                "sell": analysis.oscillators["SELL"],
                "neutral": analysis.oscillators["NEUTRAL"],
                "rsi": analysis.oscillators.get("RSI"),
                "stoch_k": analysis.oscillators.get("STOCH.K"),
                "cci": analysis.oscillators.get("CCI"),
                "adx": analysis.oscillators.get("ADX"),
                "macd": analysis.oscillators.get("MACD.macd"),
            },
            "moving_averages": {
                "recommendation": analysis.moving_averages["RECOMMENDATION"],
                "buy": analysis.moving_averages["BUY"],
                "sell": analysis.moving_averages["SELL"],
                "neutral": analysis.moving_averages["NEUTRAL"],
                "ema10": analysis.moving_averages.get("EMA10"),
                "ema20": analysis.moving_averages.get("EMA20"),
                "ema50": analysis.moving_averages.get("EMA50"),
                "ema100": analysis.moving_averages.get("EMA100"),
                "ema200": analysis.moving_averages.get("EMA200"),
                "sma10": analysis.moving_averages.get("SMA10"),
                "sma20": analysis.moving_averages.get("SMA20"),
                "sma50": analysis.moving_averages.get("SMA50"),
                "sma100": analysis.moving_averages.get("SMA100"),
                "sma200": analysis.moving_averages.get("SMA200"),
            },
            "indicators": {
                "open": analysis.indicators.get("open"),
                "high": analysis.indicators.get("high"),
                "low": analysis.indicators.get("low"),
                "close": analysis.indicators.get("close"),
                "volume": analysis.indicators.get("volume"),
                "change": analysis.indicators.get("change"),
                "change_percent": analysis.indicators.get("change|1"),
                "rsi": analysis.indicators.get("RSI"),
                "rsi7": analysis.indicators.get("RSI[1]"),
                "macd_macd": analysis.indicators.get("MACD.macd"),
                "macd_signal": analysis.indicators.get("MACD.signal"),
                "bb_upper": analysis.indicators.get("BB.upper"),
                "bb_lower": analysis.indicators.get("BB.lower"),
                "pivot_classic_s1": analysis.indicators.get("Pivot.M.Classic.S1"),
                "pivot_classic_r1": analysis.indicators.get("Pivot.M.Classic.R1"),
                "atr": analysis.indicators.get("ATR"),
                "adx": analysis.indicators.get("ADX"),
                "cci": analysis.indicators.get("CCI20"),
                "stoch_k": analysis.indicators.get("Stoch.K"),
                "stoch_d": analysis.indicators.get("Stoch.D"),
            }
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_quote(symbol: str, exchange: str = "NASDAQ", screener: str = "america") -> dict:
    """Get real-time quote for a symbol."""
    try:
        handler = TA_Handler(
            symbol=symbol.upper(),
            screener=screener.lower(),
            exchange=exchange.upper(),
            interval=Interval.INTERVAL_1_MINUTE
        )

        analysis = handler.get_analysis()
        indicators = analysis.indicators

        return {
            "symbol": symbol.upper(),
            "exchange": exchange.upper(),
            "time": datetime.now().isoformat(),
            "price": {
                "open": indicators.get("open"),
                "high": indicators.get("high"),
                "low": indicators.get("low"),
                "close": indicators.get("close"),
                "current": indicators.get("close"),
            },
            "volume": indicators.get("volume"),
            "change": indicators.get("change"),
            "change_percent": round(indicators.get("change", 0) / indicators.get("open", 1) * 100, 2) if indicators.get("open") else None,
            "52_week_high": indicators.get("price_52_week_high"),
            "52_week_low": indicators.get("price_52_week_low"),
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def search_symbols(query: str, exchange: str = None) -> dict:
    """Search for symbols on TradingView."""
    try:
        url = "https://symbol-search.tradingview.com/symbol_search/"
        params = {
            "text": query,
            "type": "stock,crypto,forex,futures,index",
            "exchange": exchange if exchange else "",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        results = []
        for item in data[:20]:  # Limit to top 20 results
            results.append({
                "symbol": item.get("symbol"),
                "description": item.get("description"),
                "exchange": item.get("exchange"),
                "type": item.get("type"),
                "currency": item.get("currency_code"),
            })

        return {
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {"error": str(e), "query": query}


def get_market_overview(market: str = "america") -> dict:
    """Get market overview with top gainers, losers, and most active."""
    try:
        # Major indices based on market
        indices = {
            "america": [
                ("SPX", "INDEX", "SP:SPX"),
                ("NDX", "INDEX", "NASDAQ:NDX"),
                ("DJI", "INDEX", "DJ:DJI"),
                ("VIX", "INDEX", "TVC:VIX"),
            ],
            "crypto": [
                ("BTCUSD", "BINANCE", "crypto"),
                ("ETHUSD", "BINANCE", "crypto"),
                ("SOLUSD", "BINANCE", "crypto"),
            ],
            "forex": [
                ("EURUSD", "FX_IDC", "forex"),
                ("GBPUSD", "FX_IDC", "forex"),
                ("USDJPY", "FX_IDC", "forex"),
            ],
        }

        market_data = {
            "market": market,
            "time": datetime.now().isoformat(),
            "indices": []
        }

        market_indices = indices.get(market.lower(), indices["america"])

        for symbol, exchange, screener in market_indices:
            try:
                if screener in ["crypto", "forex"]:
                    handler = TA_Handler(
                        symbol=symbol,
                        screener=screener,
                        exchange=exchange,
                        interval=Interval.INTERVAL_1_DAY
                    )
                else:
                    handler = TA_Handler(
                        symbol=symbol,
                        screener="america",
                        exchange=exchange.split(":")[0] if ":" in exchange else "INDEX",
                        interval=Interval.INTERVAL_1_DAY
                    )

                analysis = handler.get_analysis()
                indicators = analysis.indicators

                market_data["indices"].append({
                    "symbol": symbol,
                    "exchange": exchange,
                    "price": indicators.get("close"),
                    "change": indicators.get("change"),
                    "recommendation": analysis.summary["RECOMMENDATION"],
                })
            except Exception as e:
                market_data["indices"].append({
                    "symbol": symbol,
                    "error": str(e)
                })

        return market_data
    except Exception as e:
        return {"error": str(e), "market": market}


def get_screener(screener_type: str = "most_active", market: str = "america", limit: int = 10) -> dict:
    """Get screener results for top stocks."""
    try:
        # TradingView screener API
        url = "https://scanner.tradingview.com/america/scan"

        # Build filter based on screener type
        if screener_type == "top_gainers":
            sort_field = "change"
            sort_order = "desc"
        elif screener_type == "top_losers":
            sort_field = "change"
            sort_order = "asc"
        elif screener_type == "most_active":
            sort_field = "volume"
            sort_order = "desc"
        elif screener_type == "overbought":
            sort_field = "RSI"
            sort_order = "desc"
        elif screener_type == "oversold":
            sort_field = "RSI"
            sort_order = "asc"
        else:
            sort_field = "volume"
            sort_order = "desc"

        payload = {
            "filter": [
                {"left": "type", "operation": "in_range", "right": ["stock", "dr", "fund"]},
                {"left": "subtype", "operation": "in_range", "right": ["common", "foreign-issuer", "", "etf", "etf,odd", "etf,otc", "etf,cfd"]},
                {"left": "exchange", "operation": "in_range", "right": ["NYSE", "NASDAQ", "AMEX"]},
                {"left": "is_primary", "operation": "equal", "right": True},
                {"left": "active_symbol", "operation": "equal", "right": True}
            ],
            "options": {"lang": "en"},
            "markets": [market],
            "symbols": {"query": {"types": []}, "tickers": []},
            "columns": ["name", "close", "change", "change_abs", "volume", "Recommend.All", "RSI", "exchange"],
            "sort": {"sortBy": sort_field, "sortOrder": sort_order},
            "range": [0, limit]
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()

        results = []
        for item in data.get("data", []):
            d = item.get("d", [])
            results.append({
                "symbol": d[0] if len(d) > 0 else None,
                "price": d[1] if len(d) > 1 else None,
                "change_percent": d[2] if len(d) > 2 else None,
                "change": d[3] if len(d) > 3 else None,
                "volume": d[4] if len(d) > 4 else None,
                "recommendation": d[5] if len(d) > 5 else None,
                "rsi": d[6] if len(d) > 6 else None,
                "exchange": d[7] if len(d) > 7 else None,
            })

        return {
            "screener_type": screener_type,
            "market": market,
            "time": datetime.now().isoformat(),
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {"error": str(e), "screener_type": screener_type}


def get_crypto_analysis(symbol: str = "BTCUSD", exchange: str = "BINANCE", interval: str = "1d") -> dict:
    """Get cryptocurrency technical analysis."""
    try:
        interval_enum = INTERVAL_MAP.get(interval, Interval.INTERVAL_1_DAY)

        handler = TA_Handler(
            symbol=symbol.upper(),
            screener="crypto",
            exchange=exchange.upper(),
            interval=interval_enum
        )

        analysis = handler.get_analysis()

        return {
            "symbol": symbol.upper(),
            "exchange": exchange.upper(),
            "interval": interval,
            "time": datetime.now().isoformat(),
            "price": {
                "open": analysis.indicators.get("open"),
                "high": analysis.indicators.get("high"),
                "low": analysis.indicators.get("low"),
                "close": analysis.indicators.get("close"),
            },
            "volume": analysis.indicators.get("volume"),
            "summary": {
                "recommendation": analysis.summary["RECOMMENDATION"],
                "buy_signals": analysis.summary["BUY"],
                "sell_signals": analysis.summary["SELL"],
                "neutral_signals": analysis.summary["NEUTRAL"],
            },
            "indicators": {
                "rsi": analysis.indicators.get("RSI"),
                "macd": analysis.indicators.get("MACD.macd"),
                "macd_signal": analysis.indicators.get("MACD.signal"),
                "bb_upper": analysis.indicators.get("BB.upper"),
                "bb_lower": analysis.indicators.get("BB.lower"),
                "ema20": analysis.indicators.get("EMA20"),
                "sma20": analysis.indicators.get("SMA20"),
            }
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_forex_analysis(pair: str = "EURUSD", interval: str = "1d") -> dict:
    """Get forex pair technical analysis."""
    try:
        interval_enum = INTERVAL_MAP.get(interval, Interval.INTERVAL_1_DAY)

        handler = TA_Handler(
            symbol=pair.upper(),
            screener="forex",
            exchange="FX_IDC",
            interval=interval_enum
        )

        analysis = handler.get_analysis()

        return {
            "pair": pair.upper(),
            "interval": interval,
            "time": datetime.now().isoformat(),
            "price": {
                "open": analysis.indicators.get("open"),
                "high": analysis.indicators.get("high"),
                "low": analysis.indicators.get("low"),
                "close": analysis.indicators.get("close"),
            },
            "summary": {
                "recommendation": analysis.summary["RECOMMENDATION"],
                "buy_signals": analysis.summary["BUY"],
                "sell_signals": analysis.summary["SELL"],
                "neutral_signals": analysis.summary["NEUTRAL"],
            },
            "pivot_points": {
                "classic_s3": analysis.indicators.get("Pivot.M.Classic.S3"),
                "classic_s2": analysis.indicators.get("Pivot.M.Classic.S2"),
                "classic_s1": analysis.indicators.get("Pivot.M.Classic.S1"),
                "classic_p": analysis.indicators.get("Pivot.M.Classic.Middle"),
                "classic_r1": analysis.indicators.get("Pivot.M.Classic.R1"),
                "classic_r2": analysis.indicators.get("Pivot.M.Classic.R2"),
                "classic_r3": analysis.indicators.get("Pivot.M.Classic.R3"),
            },
            "indicators": {
                "rsi": analysis.indicators.get("RSI"),
                "stoch_k": analysis.indicators.get("Stoch.K"),
                "stoch_d": analysis.indicators.get("Stoch.D"),
                "cci": analysis.indicators.get("CCI20"),
                "adx": analysis.indicators.get("ADX"),
                "atr": analysis.indicators.get("ATR"),
            }
        }
    except Exception as e:
        return {"error": str(e), "pair": pair}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available TradingView tools."""
    return [
        Tool(
            name="get_technical_analysis",
            description="Get comprehensive technical analysis for a stock symbol including oscillators, moving averages, and trading recommendations from TradingView.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., AAPL, MSFT, GOOGL)"
                    },
                    "exchange": {
                        "type": "string",
                        "description": "The exchange (e.g., NASDAQ, NYSE, AMEX)",
                        "default": "NASDAQ"
                    },
                    "screener": {
                        "type": "string",
                        "description": "The market screener (e.g., america, india, crypto)",
                        "default": "america"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w, 1M)",
                        "default": "1d"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_quote",
            description="Get real-time quote and price information for a stock symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (e.g., AAPL, TSLA)"
                    },
                    "exchange": {
                        "type": "string",
                        "description": "The exchange (e.g., NASDAQ, NYSE)",
                        "default": "NASDAQ"
                    },
                    "screener": {
                        "type": "string",
                        "description": "The market screener",
                        "default": "america"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="search_symbols",
            description="Search for stock, crypto, forex, or futures symbols on TradingView.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (e.g., Apple, Bitcoin, EURUSD)"
                    },
                    "exchange": {
                        "type": "string",
                        "description": "Filter by exchange (optional)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_market_overview",
            description="Get market overview including major indices performance.",
            inputSchema={
                "type": "object",
                "properties": {
                    "market": {
                        "type": "string",
                        "description": "The market (america, crypto, forex)",
                        "default": "america"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_screener",
            description="Get screener results for top stocks (gainers, losers, most active, overbought, oversold).",
            inputSchema={
                "type": "object",
                "properties": {
                    "screener_type": {
                        "type": "string",
                        "description": "Type of screener (top_gainers, top_losers, most_active, overbought, oversold)",
                        "default": "most_active"
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to screen",
                        "default": "america"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 10
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_crypto_analysis",
            description="Get technical analysis for a cryptocurrency.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The crypto symbol (e.g., BTCUSD, ETHUSD)",
                        "default": "BTCUSD"
                    },
                    "exchange": {
                        "type": "string",
                        "description": "The exchange (e.g., BINANCE, COINBASE)",
                        "default": "BINANCE"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w, 1M)",
                        "default": "1d"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_forex_analysis",
            description="Get technical analysis for a forex currency pair.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pair": {
                        "type": "string",
                        "description": "The forex pair (e.g., EURUSD, GBPUSD, USDJPY)",
                        "default": "EURUSD"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Time interval (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w, 1M)",
                        "default": "1d"
                    }
                },
                "required": []
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution."""
    try:
        if name == "get_technical_analysis":
            result = get_technical_analysis(
                symbol=arguments["symbol"],
                exchange=arguments.get("exchange", "NASDAQ"),
                screener=arguments.get("screener", "america"),
                interval=arguments.get("interval", "1d")
            )
        elif name == "get_quote":
            result = get_quote(
                symbol=arguments["symbol"],
                exchange=arguments.get("exchange", "NASDAQ"),
                screener=arguments.get("screener", "america")
            )
        elif name == "search_symbols":
            result = search_symbols(
                query=arguments["query"],
                exchange=arguments.get("exchange")
            )
        elif name == "get_market_overview":
            result = get_market_overview(
                market=arguments.get("market", "america")
            )
        elif name == "get_screener":
            result = get_screener(
                screener_type=arguments.get("screener_type", "most_active"),
                market=arguments.get("market", "america"),
                limit=arguments.get("limit", 10)
            )
        elif name == "get_crypto_analysis":
            result = get_crypto_analysis(
                symbol=arguments.get("symbol", "BTCUSD"),
                exchange=arguments.get("exchange", "BINANCE"),
                interval=arguments.get("interval", "1d")
            )
        elif name == "get_forex_analysis":
            result = get_forex_analysis(
                pair=arguments.get("pair", "EURUSD"),
                interval=arguments.get("interval", "1d")
            )
        else:
            result = {"error": f"Unknown tool: {name}"}

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str)
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
