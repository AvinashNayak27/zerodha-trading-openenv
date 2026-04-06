"""
Pydantic models for the Zerodha Trading Environment.
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class ActionType(str, Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    MODIFY = "MODIFY"
    HEDGE = "HEDGE"
    HOLD = "HOLD"

class Segment(str, Enum):
    EQ = "EQ"
    FO = "FO"
    COM = "COM"

class PositionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    SL_HIT = "SL_HIT"
    TARGET_HIT = "TARGET_HIT"


class Order(BaseModel):
    order_id: str
    instrument: str
    segment: Segment
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: float
    timestamp: int

class Position(BaseModel):
    position_id: str
    instrument: str
    segment: Segment
    side: OrderSide
    quantity: int
    entry_price: float
    entry_candle: int
    stoploss: Optional[float] = None
    target: Optional[float] = None
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    margin_used: float = 0.0
    status: PositionStatus = PositionStatus.OPEN

class PortfolioState(BaseModel):
    capital: float
    available_capital: float
    margin_used: float
    positions: Dict[str, Position] = Field(default_factory=dict)
    closed_positions: List[Position] = Field(default_factory=list)
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    peak_capital: float = 0.0
    max_drawdown: float = 0.0
    total_trades: int = 0
    winning_trades: int = 0


class TradingAction(BaseModel):
    action_type: ActionType = ActionType.HOLD
    instrument: Optional[str] = None
    segment: Optional[Segment] = None
    side: Optional[OrderSide] = None
    quantity: Optional[int] = None
    order_type: OrderType = OrderType.MARKET
    limit_price: Optional[float] = None
    stoploss: Optional[float] = None
    target: Optional[float] = None
    position_id: Optional[str] = None
    new_stoploss: Optional[float] = None
    new_target: Optional[float] = None

class Candle(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float

class TradingObservation(BaseModel):
    step: int
    max_steps: int
    task_id: str
    candle_index: int
    instruments: List[str]
    candles: Dict[str, List[Candle]]
    portfolio: PortfolioState
    last_action_result: Optional[str] = None
    reward: float = 0.0
    done: bool = False
    info: Dict = Field(default_factory=dict)
