"""
OHLCV data loader using yfinance as the price proxy for all 72 instruments.
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple

import pandas as pd
import yfinance as yf

from zerodha_trading_env.data.instruments import get_yf_ticker, INSTRUMENTS

logger = logging.getLogger(__name__)


class DataUnavailableError(Exception):
    pass


_CACHE: Dict[Tuple[str, str, str, str], List[dict]] = {}
CACHE_MAX_ENTRIES = 500


def _cache_key(ticker, interval, start, end):
    return (ticker, interval, start, end)


def _evict_if_needed():
    if len(_CACHE) > CACHE_MAX_ENTRIES:
        remove = list(_CACHE.keys())[: CACHE_MAX_ENTRIES // 4]
        for k in remove:
            del _CACHE[k]


def _fetch_yf(ticker: str, start: str, end: str, interval: str = "1d") -> List[dict]:
    key = _cache_key(ticker, interval, start, end)
    if key in _CACHE:
        return _CACHE[key]

    logger.info("Fetching yfinance: %s | %s | %s -> %s", ticker, interval, start, end)
    try:
        df = yf.download(ticker, start=start, end=end, interval=interval, progress=False, auto_adjust=True)
    except Exception as exc:
        raise DataUnavailableError(f"yfinance error for {ticker}: {exc}") from exc

    if df is None or df.empty:
        raise DataUnavailableError(f"No data returned by yfinance for {ticker}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df = df.sort_index()
    candles = []
    for ts, row in df.iterrows():
        def _f(col):
            val = row.get(col, 0.0)
            if hasattr(val, "iloc"):
                val = val.iloc[0]
            return float(val) if val is not None else 0.0
        candles.append({
            "timestamp": str(ts.date()) if hasattr(ts, "date") else str(ts),
            "open": _f("Open"), "high": _f("High"),
            "low": _f("Low"), "close": _f("Close"), "volume": _f("Volume"),
        })

    _evict_if_needed()
    _CACHE[key] = candles
    return candles


def get_candles(symbol: str, start=None, end=None, n_candles=None, interval="1d") -> List[dict]:
    ticker = get_yf_ticker(symbol)
    today = date.today()
    end = end or str(today)
    start = start or str(today - timedelta(days=730))
    candles = _fetch_yf(ticker, start, end, interval)
    if n_candles is not None:
        candles = candles[-n_candles:]
    return candles


def get_candles_for_symbols(symbols, start=None, end=None, n_candles=None, interval="1d") -> Dict[str, List[dict]]:
    ticker_to_symbols: Dict[str, List[str]] = {}
    for sym in symbols:
        tk = get_yf_ticker(sym)
        ticker_to_symbols.setdefault(tk, []).append(sym)

    today = date.today()
    _end = end or str(today)
    _start = start or str(today - timedelta(days=730))

    result: Dict[str, List[dict]] = {}
    for ticker, syms in ticker_to_symbols.items():
        try:
            candles = _fetch_yf(ticker, _start, _end, interval)
            if n_candles is not None:
                candles = candles[-n_candles:]
        except DataUnavailableError as exc:
            logger.warning("No data for ticker %s: %s", ticker, exc)
            candles = []
        for sym in syms:
            result[sym] = candles
    return result


def get_latest_price(symbol: str) -> float:
    today = date.today()
    candles = get_candles(symbol, start=str(today - timedelta(days=7)), end=str(today + timedelta(days=1)))
    if not candles:
        raise DataUnavailableError(f"Cannot get latest price for {symbol}")
    return candles[-1]["close"]


def clear_cache():
    _CACHE.clear()


def cache_stats() -> dict:
    return {"entries": len(_CACHE), "max_entries": CACHE_MAX_ENTRIES}
