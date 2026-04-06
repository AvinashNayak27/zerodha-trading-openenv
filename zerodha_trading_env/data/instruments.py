"""
All 72 instruments traded on Zerodha.
"""

from __future__ import annotations
from typing import Dict, Any

INSTRUMENTS: Dict[str, Dict[str, Any]] = {
    # EQ
    "BAJFINANCE": {"segment": "EQ", "yf_ticker": "BAJFINANCE.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Bajaj Finance Ltd"},
    "GRASIM": {"segment": "EQ", "yf_ticker": "GRASIM.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Grasim Industries Ltd"},
    "HINDALCO": {"segment": "EQ", "yf_ticker": "HINDALCO.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Hindalco Industries Ltd"},
    "KOTAKBANK": {"segment": "EQ", "yf_ticker": "KOTAKBANK.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Kotak Mahindra Bank Ltd"},
    "LT": {"segment": "EQ", "yf_ticker": "LT.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Larsen & Toubro Ltd"},
    "MAZDOCK": {"segment": "EQ", "yf_ticker": "MAZDOCK.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Mazagon Dock Shipbuilders Ltd"},
    "SAREGAMA": {"segment": "EQ", "yf_ticker": "SAREGAMA.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Saregama India Ltd"},
    "TATASTEEL": {"segment": "EQ", "yf_ticker": "TATASTEEL.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Tata Steel Ltd"},
    "TRIVENI": {"segment": "EQ", "yf_ticker": "TRIVENI.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Triveni Engineering & Industries"},
    "VEDL": {"segment": "EQ", "yf_ticker": "VEDL.NS", "lot_size": 1, "margin_pct": 0.20, "description": "Vedanta Ltd"},
    # FO
    "NIFTY25APRFUT": {"segment": "FO", "yf_ticker": "^NSEI", "lot_size": 75, "margin_pct": 0.12, "description": "Nifty Apr 2025 Futures"},
    "NIFTY25MAYFUT": {"segment": "FO", "yf_ticker": "^NSEI", "lot_size": 75, "margin_pct": 0.12, "description": "Nifty May 2025 Futures"},
    "NIFTY25JUNFUT": {"segment": "FO", "yf_ticker": "^NSEI", "lot_size": 75, "margin_pct": 0.12, "description": "Nifty Jun 2025 Futures"},
    "NIFTY25JULFUT": {"segment": "FO", "yf_ticker": "^NSEI", "lot_size": 75, "margin_pct": 0.12, "description": "Nifty Jul 2025 Futures"},
    "NIFTY25AUGFUT": {"segment": "FO", "yf_ticker": "^NSEI", "lot_size": 75, "margin_pct": 0.12, "description": "Nifty Aug 2025 Futures"},
    "NIFTY25SEPFUT": {"segment": "FO", "yf_ticker": "^NSEI", "lot_size": 75, "margin_pct": 0.12, "description": "Nifty Sep 2025 Futures"},
    "BANKNIFTY25APRFUT": {"segment": "FO", "yf_ticker": "^NSEBANK", "lot_size": 35, "margin_pct": 0.12, "description": "Bank Nifty Apr 2025 Futures"},
    "BANKNIFTY25DEC60000CE": {"segment": "FO", "yf_ticker": "^NSEBANK", "lot_size": 35, "margin_pct": 0.15, "description": "Bank Nifty Dec 2025 60000 CE"},
    "BANKNIFTY25MAY56000CE": {"segment": "FO", "yf_ticker": "^NSEBANK", "lot_size": 35, "margin_pct": 0.15, "description": "Bank Nifty May 2025 56000 CE"},
    "BANKNIFTY25MAR56000CE": {"segment": "FO", "yf_ticker": "^NSEBANK", "lot_size": 35, "margin_pct": 0.15, "description": "Bank Nifty Mar 2025 56000 CE"},
    "BANKNIFTY25APR55000CE": {"segment": "FO", "yf_ticker": "^NSEBANK", "lot_size": 35, "margin_pct": 0.15, "description": "Bank Nifty Apr 2025 55000 CE"},
    "BAJAJ-AUTO26MARFUT": {"segment": "FO", "yf_ticker": "BAJAJ-AUTO.NS", "lot_size": 75, "margin_pct": 0.12, "description": "Bajaj Auto Mar 2026 Futures"},
    "BAJAJFINSV26MARFUT": {"segment": "FO", "yf_ticker": "BAJAJFINSV.NS", "lot_size": 125, "margin_pct": 0.12, "description": "Bajaj Finserv Mar 2026 Futures"},
    "BHARTIARTL25APRFUT": {"segment": "FO", "yf_ticker": "BHARTIARTL.NS", "lot_size": 500, "margin_pct": 0.12, "description": "Bharti Airtel Apr 2025 Futures"},
    "BHARTIARTL25MAYFUT": {"segment": "FO", "yf_ticker": "BHARTIARTL.NS", "lot_size": 500, "margin_pct": 0.12, "description": "Bharti Airtel May 2025 Futures"},
    "BHARTIARTL25JULFUT": {"segment": "FO", "yf_ticker": "BHARTIARTL.NS", "lot_size": 500, "margin_pct": 0.12, "description": "Bharti Airtel Jul 2025 Futures"},
    "DIXON25JUNFUT": {"segment": "FO", "yf_ticker": "DIXON.NS", "lot_size": 75, "margin_pct": 0.12, "description": "Dixon Technologies Jun 2025 Futures"},
    "EICHERMOT25JUNFUT": {"segment": "FO", "yf_ticker": "EICHERMOT.NS", "lot_size": 150, "margin_pct": 0.12, "description": "Eicher Motors Jun 2025 Futures"},
    "HINDALCO25SEPFUT": {"segment": "FO", "yf_ticker": "HINDALCO.NS", "lot_size": 2750, "margin_pct": 0.12, "description": "Hindalco Sep 2025 Futures"},
    "IEX25JUNFUT": {"segment": "FO", "yf_ticker": "IEX.NS", "lot_size": 3750, "margin_pct": 0.12, "description": "Indian Energy Exchange Jun 2025 Futures"},
    "INDIANB25JUNFUT": {"segment": "FO", "yf_ticker": "INDIANB.NS", "lot_size": 1500, "margin_pct": 0.12, "description": "Indian Bank Jun 2025 Futures"},
    "INDIGO25JUNFUT": {"segment": "FO", "yf_ticker": "INDIGO.NS", "lot_size": 300, "margin_pct": 0.12, "description": "IndiGo Jun 2025 Futures"},
    "LAURUSLABS25JUNFUT": {"segment": "FO", "yf_ticker": "LAURUSLABS.NS", "lot_size": 1500, "margin_pct": 0.12, "description": "Laurus Labs Jun 2025 Futures"},
    "LT25NOVFUT": {"segment": "FO", "yf_ticker": "LT.NS", "lot_size": 375, "margin_pct": 0.12, "description": "L&T Nov 2025 Futures"},
    "MCX25JUNFUT": {"segment": "FO", "yf_ticker": "MCX.NS", "lot_size": 250, "margin_pct": 0.12, "description": "MCX India Jun 2025 Futures"},
    "PATANJALI25APRFUT": {"segment": "FO", "yf_ticker": "PATANJALI.NS", "lot_size": 500, "margin_pct": 0.12, "description": "Patanjali Foods Apr 2025 Futures"},
    "PATANJALI25MAYFUT": {"segment": "FO", "yf_ticker": "PATANJALI.NS", "lot_size": 500, "margin_pct": 0.12, "description": "Patanjali Foods May 2025 Futures"},
    "PATANJALI25SEPFUT": {"segment": "FO", "yf_ticker": "PATANJALI.NS", "lot_size": 500, "margin_pct": 0.12, "description": "Patanjali Foods Sep 2025 Futures"},
    "SRF25JUNFUT": {"segment": "FO", "yf_ticker": "SRF.NS", "lot_size": 375, "margin_pct": 0.12, "description": "SRF Ltd Jun 2025 Futures"},
    "TATASTEEL25SEPFUT": {"segment": "FO", "yf_ticker": "TATASTEEL.NS", "lot_size": 5500, "margin_pct": 0.12, "description": "Tata Steel Sep 2025 Futures"},
    "TVSMOTOR25JUNFUT": {"segment": "FO", "yf_ticker": "TVSMOTOR.NS", "lot_size": 350, "margin_pct": 0.12, "description": "TVS Motor Jun 2025 Futures"},
    "VEDL25JULFUT": {"segment": "FO", "yf_ticker": "VEDL.NS", "lot_size": 2000, "margin_pct": 0.12, "description": "Vedanta Jul 2025 Futures"},
    # COM
    "GOLD25AUGFUT": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.05, "description": "MCX Gold Aug 2025 Futures"},
    "GOLD25DECFUT": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.05, "description": "MCX Gold Dec 2025 Futures"},
    "GOLD25OCTFUT": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.05, "description": "MCX Gold Oct 2025 Futures"},
    "GOLD26APRFUT": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.05, "description": "MCX Gold Apr 2026 Futures"},
    "GOLD26FEBFUT": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.05, "description": "MCX Gold Feb 2026 Futures"},
    "GOLD26JUNFUT": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.05, "description": "MCX Gold Jun 2026 Futures"},
    "GOLD25OCT123000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Oct 2025 123000 CE"},
    "GOLD25OCT124000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Oct 2025 124000 CE"},
    "GOLD25NOV121000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Nov 2025 121000 CE"},
    "GOLD25NOV122000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Nov 2025 122000 CE"},
    "GOLD25NOV125000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Nov 2025 125000 CE"},
    "GOLD25NOV127000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Nov 2025 127000 CE"},
    "GOLD26JAN139000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Jan 2026 139000 CE"},
    "GOLD25DEC131000CE": {"segment": "COM", "yf_ticker": "GC=F", "lot_size": 1, "margin_pct": 0.10, "description": "MCX Gold Dec 2025 131000 CE"},
    "SILVER25JULFUT": {"segment": "COM", "yf_ticker": "SI=F", "lot_size": 30, "margin_pct": 0.05, "description": "MCX Silver Jul 2025 Futures"},
    "SILVER26MARFUT": {"segment": "COM", "yf_ticker": "SI=F", "lot_size": 30, "margin_pct": 0.05, "description": "MCX Silver Mar 2026 Futures"},
    "SILVER25APR94000CE": {"segment": "COM", "yf_ticker": "SI=F", "lot_size": 30, "margin_pct": 0.10, "description": "MCX Silver Apr 2025 94000 CE"},
    "COPPER25AUGFUT": {"segment": "COM", "yf_ticker": "HG=F", "lot_size": 2500, "margin_pct": 0.05, "description": "MCX Copper Aug 2025 Futures"},
    "COPPER25JULFUT": {"segment": "COM", "yf_ticker": "HG=F", "lot_size": 2500, "margin_pct": 0.05, "description": "MCX Copper Jul 2025 Futures"},
    "COPPER26FEBFUT": {"segment": "COM", "yf_ticker": "HG=F", "lot_size": 2500, "margin_pct": 0.05, "description": "MCX Copper Feb 2026 Futures"},
    "COPPER26MARFUT": {"segment": "COM", "yf_ticker": "HG=F", "lot_size": 2500, "margin_pct": 0.05, "description": "MCX Copper Mar 2026 Futures"},
    "ALUMINIUM25OCTFUT": {"segment": "COM", "yf_ticker": "ALI=F", "lot_size": 5000, "margin_pct": 0.05, "description": "MCX Aluminium Oct 2025 Futures"},
    "ALUMINIUM25SEPFUT": {"segment": "COM", "yf_ticker": "ALI=F", "lot_size": 5000, "margin_pct": 0.05, "description": "MCX Aluminium Sep 2025 Futures"},
    "CRUDEOIL25MAYFUT": {"segment": "COM", "yf_ticker": "CL=F", "lot_size": 100, "margin_pct": 0.05, "description": "MCX Crude Oil May 2025 Futures"},
    "CRUDEOIL26JANFUT": {"segment": "COM", "yf_ticker": "CL=F", "lot_size": 100, "margin_pct": 0.05, "description": "MCX Crude Oil Jan 2026 Futures"},
    "CRUDEOIL26MARFUT": {"segment": "COM", "yf_ticker": "CL=F", "lot_size": 100, "margin_pct": 0.05, "description": "MCX Crude Oil Mar 2026 Futures"},
    "CRUDEOIL25APR5000PE": {"segment": "COM", "yf_ticker": "CL=F", "lot_size": 100, "margin_pct": 0.10, "description": "MCX Crude Oil Apr 2025 5000 PE"},
    "NATURALGAS25JUNFUT": {"segment": "COM", "yf_ticker": "NG=F", "lot_size": 1250, "margin_pct": 0.05, "description": "MCX Natural Gas Jun 2025 Futures"},
    "LEAD25JUNFUT": {"segment": "COM", "yf_ticker": "PA=F", "lot_size": 5000, "margin_pct": 0.05, "description": "MCX Lead Jun 2025 Futures"},
    "ZINC25JUNFUT": {"segment": "COM", "yf_ticker": "ZNC=F", "lot_size": 5000, "margin_pct": 0.05, "description": "MCX Zinc Jun 2025 Futures"},
}

def get_instrument(symbol: str):
    if symbol not in INSTRUMENTS:
        raise KeyError(f"Unknown instrument: {symbol}")
    return INSTRUMENTS[symbol]

def get_yf_ticker(symbol: str) -> str:
    return get_instrument(symbol)["yf_ticker"]

def get_segment(symbol: str) -> str:
    return get_instrument(symbol)["segment"]

def get_lot_size(symbol: str) -> int:
    return get_instrument(symbol)["lot_size"]

def get_margin_pct(symbol: str) -> float:
    return get_instrument(symbol)["margin_pct"]

def list_by_segment(segment: str):
    return [s for s, v in INSTRUMENTS.items() if v["segment"] == segment]

ALL_SYMBOLS = list(INSTRUMENTS.keys())
EQ_SYMBOLS  = list_by_segment("EQ")
FO_SYMBOLS  = list_by_segment("FO")
COM_SYMBOLS = list_by_segment("COM")
