"""
ZerodhaTradingEnv - core historical replay environment.
"""

from __future__ import annotations

import uuid
import logging
from typing import Dict, List, Optional, Any

from zerodha_trading_env.models import (
    TradingAction, TradingObservation, PortfolioState,
    Position, Order, Candle,
    ActionType, OrderSide, OrderType, PositionStatus, Segment,
)
from zerodha_trading_env.data.instruments import (
    get_lot_size, get_margin_pct, get_segment, INSTRUMENTS,
    EQ_SYMBOLS, COM_SYMBOLS, ALL_SYMBOLS,
)
from zerodha_trading_env.data.loader import get_candles_for_symbols, DataUnavailableError

logger = logging.getLogger(__name__)

TASK_CONFIGS: Dict[str, Dict[str, Any]] = {
    "task_1_single_trade": {
        "name": "Single Trade Efficiency",
        "difficulty": "easy",
        "max_steps": 20,
        "initial_capital": 500_000,
        "instruments": ["GOLD26JUNFUT"],
        "max_positions": 1,
        "n_candles_history": 50,
        "candle_window": 50,
    },
    "task_2_portfolio": {
        "name": "Multi-Position Portfolio Management",
        "difficulty": "medium",
        "max_steps": 50,
        "initial_capital": 2_000_000,
        "instruments": EQ_SYMBOLS + COM_SYMBOLS[:5],
        "max_positions": 5,
        "n_candles_history": 20,
        "candle_window": 100,
    },
    "task_3_full_session": {
        "name": "Full Trading Session",
        "difficulty": "hard",
        "max_steps": 100,
        "initial_capital": 5_000_000,
        "instruments": ALL_SYMBOLS,
        "max_positions": 20,
        "n_candles_history": 10,
        "candle_window": 200,
    },
}

MAX_CONCURRENT_POSITIONS_DEFAULT = 10
SLIPPAGE_PCT = 0.0005


class ZerodhaTradingEnv:
    """Historical replay trading environment."""

    def __init__(self):
        self._task_id: Optional[str] = None
        self._task_cfg: Optional[Dict] = None
        self._candles: Dict[str, List[dict]] = {}
        self._candle_idx: int = 0
        self._step: int = 0
        self._portfolio: Optional[PortfolioState] = None
        self._orders: List[Order] = []
        self._instruments: List[str] = []
        self._done: bool = False
        self._last_result: str = ""
        self._prev_equity: float = 0.0
        self._total_margin_deployed: float = 0.0

    def reset(self, task_id: str = "task_1_single_trade", config: Optional[Dict] = None) -> TradingObservation:
        if task_id not in TASK_CONFIGS:
            raise ValueError(f"Unknown task_id '{task_id}'.")

        self._task_id = task_id
        self._task_cfg = {**TASK_CONFIGS[task_id], **(config or {})}
        cfg = self._task_cfg

        self._instruments = list(cfg["instruments"])
        initial_capital = float(cfg["initial_capital"])
        candle_window = int(cfg["candle_window"])

        try:
            raw = get_candles_for_symbols(self._instruments, n_candles=candle_window + cfg["n_candles_history"])
        except DataUnavailableError as exc:
            logger.warning("Data fetch failed: %s", exc)
            raw = {sym: [] for sym in self._instruments}

        self._candles = {}
        for sym in self._instruments:
            data = raw.get(sym, [])
            if len(data) < 2:
                data = _synthetic_candles(100.0, candle_window + cfg["n_candles_history"])
            self._candles[sym] = data

        self._candle_idx = cfg["n_candles_history"]
        self._step = 0
        self._done = False
        self._last_result = "Episode started."
        self._orders = []
        self._total_margin_deployed = 0.0

        self._portfolio = PortfolioState(
            capital=initial_capital,
            available_capital=initial_capital,
            margin_used=0.0,
            peak_capital=initial_capital,
        )
        self._prev_equity = initial_capital

        return self._build_observation(reward=0.0)

    def step(self, action: TradingAction) -> TradingObservation:
        if self._done:
            raise RuntimeError("Episode is done. Call reset() first.")

        cfg = self._task_cfg
        result_msg = self._process_action(action)
        self._last_result = result_msg

        self._candle_idx += 1
        self._step += 1

        sl_msg = self._check_sl_target()
        if sl_msg:
            self._last_result += " | " + sl_msg

        self._update_unrealized_pnl()
        reward = self._compute_reward()

        max_steps = int(cfg["max_steps"])
        candle_exhausted = self._candle_idx >= len(next(iter(self._candles.values()), []))
        self._done = (self._step >= max_steps) or candle_exhausted or (self._portfolio.available_capital <= 0)

        if self._done:
            self._force_close_all()

        return self._build_observation(reward=reward)

    def _process_action(self, action: TradingAction) -> str:
        at = action.action_type
        portfolio = self._portfolio

        if at == ActionType.HOLD:
            return "HOLD"
        elif at == ActionType.OPEN:
            return self._open_position(action)
        elif at == ActionType.CLOSE:
            if not action.position_id:
                return "CLOSE failed: position_id required."
            return self._close_position(action.position_id, reason="agent_close")
        elif at == ActionType.MODIFY:
            if not action.position_id:
                return "MODIFY failed: position_id required."
            pos = portfolio.positions.get(action.position_id)
            if not pos:
                return f"MODIFY failed: position {action.position_id} not found."
            if action.new_stoploss is not None:
                pos.stoploss = action.new_stoploss
            if action.new_target is not None:
                pos.target = action.new_target
            return f"MODIFY OK: pos={action.position_id}"
        elif at == ActionType.HEDGE:
            if not action.position_id:
                return "HEDGE failed: position_id required."
            pos = portfolio.positions.get(action.position_id)
            if not pos:
                return f"HEDGE failed: position {action.position_id} not found."
            hedge_action = TradingAction(
                action_type=ActionType.OPEN,
                instrument=pos.instrument,
                segment=pos.segment,
                side=OrderSide.SELL if pos.side == OrderSide.BUY else OrderSide.BUY,
                quantity=pos.quantity,
                stoploss=action.stoploss,
                target=action.target,
            )
            return "HEDGE: " + self._open_position(hedge_action)
        return f"Unknown action type: {at}"

    def _open_position(self, action: TradingAction) -> str:
        cfg = self._task_cfg
        portfolio = self._portfolio

        if not action.instrument or action.instrument not in self._instruments:
            return f"OPEN failed: instrument '{action.instrument}' not valid."
        if not action.side:
            return "OPEN failed: side required."
        if not action.quantity or action.quantity <= 0:
            return "OPEN failed: quantity must be > 0."

        max_pos = int(cfg.get("max_positions", MAX_CONCURRENT_POSITIONS_DEFAULT))
        open_count = len([p for p in portfolio.positions.values() if p.status == PositionStatus.OPEN])
        if open_count >= max_pos:
            return f"OPEN failed: max concurrent positions ({max_pos}) reached."

        candles = self._candles[action.instrument]
        if self._candle_idx >= len(candles):
            return "OPEN failed: no candle data."
        candle = candles[self._candle_idx]
        exec_price = candle["close"]

        if action.side == OrderSide.BUY:
            exec_price *= (1 + SLIPPAGE_PCT)
        else:
            exec_price *= (1 - SLIPPAGE_PCT)

        if action.order_type == OrderType.LIMIT and action.limit_price:
            exec_price = action.limit_price

        lot = get_lot_size(action.instrument)
        notional = exec_price * action.quantity * lot
        margin = notional * get_margin_pct(action.instrument)

        if margin > portfolio.available_capital:
            return f"OPEN failed: margin {margin:.0f} > available {portfolio.available_capital:.0f}."

        portfolio.available_capital -= margin
        portfolio.margin_used += margin
        self._total_margin_deployed += margin

        pos_id = str(uuid.uuid4())[:8]
        pos = Position(
            position_id=pos_id,
            instrument=action.instrument,
            segment=Segment(get_segment(action.instrument)),
            side=action.side,
            quantity=action.quantity,
            entry_price=exec_price,
            entry_candle=self._candle_idx,
            stoploss=action.stoploss,
            target=action.target,
            current_price=exec_price,
            margin_used=margin,
            status=PositionStatus.OPEN,
        )
        portfolio.positions[pos_id] = pos
        portfolio.total_trades += 1

        order = Order(
            order_id=str(uuid.uuid4())[:8],
            instrument=action.instrument,
            segment=Segment(get_segment(action.instrument)),
            side=action.side,
            order_type=action.order_type,
            quantity=action.quantity,
            price=exec_price,
            timestamp=self._candle_idx,
        )
        self._orders.append(order)

        return f"OPEN {action.side} {action.quantity}x{action.instrument} @ {exec_price:.2f} | margin={margin:.0f} | pos_id={pos_id}"

    def _close_position(self, position_id: str, reason: str = "agent_close") -> str:
        portfolio = self._portfolio
        pos = portfolio.positions.get(position_id)
        if not pos or pos.status != PositionStatus.OPEN:
            return f"CLOSE failed: position {position_id} not open."

        candles = self._candles[pos.instrument]
        idx = min(self._candle_idx, len(candles) - 1)
        candle = candles[idx]
        exec_price = candle["close"]

        lot = get_lot_size(pos.instrument)
        if pos.side == OrderSide.BUY:
            pnl = (exec_price - pos.entry_price) * pos.quantity * lot
        else:
            pnl = (pos.entry_price - exec_price) * pos.quantity * lot

        pos.realized_pnl = pnl
        pos.current_price = exec_price
        pos.unrealized_pnl = 0.0
        pos.status = {
            "agent_close": PositionStatus.CLOSED,
            "sl_hit": PositionStatus.SL_HIT,
            "target_hit": PositionStatus.TARGET_HIT,
            "force_close": PositionStatus.CLOSED,
        }.get(reason, PositionStatus.CLOSED)

        portfolio.available_capital += pos.margin_used + pnl
        portfolio.capital += pnl
        portfolio.margin_used -= pos.margin_used
        portfolio.realized_pnl += pnl

        if pnl > 0:
            portfolio.winning_trades += 1

        if portfolio.capital > portfolio.peak_capital:
            portfolio.peak_capital = portfolio.capital
        dd = (portfolio.peak_capital - portfolio.capital) / portfolio.peak_capital
        if dd > portfolio.max_drawdown:
            portfolio.max_drawdown = dd

        portfolio.closed_positions.append(pos)
        del portfolio.positions[position_id]

        return f"CLOSE {pos.instrument} pos={position_id} @ {exec_price:.2f} pnl={pnl:+.0f} reason={reason}"

    def _check_sl_target(self) -> str:
        msgs = []
        portfolio = self._portfolio
        for pos_id, pos in list(portfolio.positions.items()):
            if pos.status != PositionStatus.OPEN:
                continue
            candles = self._candles.get(pos.instrument, [])
            idx = min(self._candle_idx, len(candles) - 1)
            if idx < 0:
                continue
            candle = candles[idx]
            low, high = candle["low"], candle["high"]

            hit_sl = hit_target = False
            if pos.side == OrderSide.BUY:
                if pos.stoploss and low <= pos.stoploss:
                    hit_sl = True
                if pos.target and high >= pos.target:
                    hit_target = True
            else:
                if pos.stoploss and high >= pos.stoploss:
                    hit_sl = True
                if pos.target and low <= pos.target:
                    hit_target = True

            if hit_sl:
                msgs.append(self._close_position(pos_id, reason="sl_hit"))
            elif hit_target:
                msgs.append(self._close_position(pos_id, reason="target_hit"))

        return " | ".join(msgs)

    def _update_unrealized_pnl(self):
        portfolio = self._portfolio
        total_unrealized = 0.0
        for pos in portfolio.positions.values():
            if pos.status != PositionStatus.OPEN:
                continue
            candles = self._candles.get(pos.instrument, [])
            idx = min(self._candle_idx, len(candles) - 1)
            if idx < 0:
                continue
            price = candles[idx]["close"]
            lot = get_lot_size(pos.instrument)
            if pos.side == OrderSide.BUY:
                upnl = (price - pos.entry_price) * pos.quantity * lot
            else:
                upnl = (pos.entry_price - price) * pos.quantity * lot
            pos.current_price = price
            pos.unrealized_pnl = upnl
            total_unrealized += upnl
        portfolio.unrealized_pnl = total_unrealized

    def _compute_reward(self) -> float:
        portfolio = self._portfolio
        equity = portfolio.capital + portfolio.unrealized_pnl
        delta = equity - self._prev_equity
        denom = max(self._total_margin_deployed, 1.0)
        reward = delta / denom
        self._prev_equity = equity
        return float(reward)

    def _force_close_all(self):
        for pos_id in list(self._portfolio.positions.keys()):
            self._close_position(pos_id, reason="force_close")

    def _build_observation(self, reward: float) -> TradingObservation:
        cfg = self._task_cfg
        hist = int(cfg["n_candles_history"])

        candle_view: Dict[str, List[Candle]] = {}
        for sym in self._instruments:
            raw = self._candles.get(sym, [])
            start = max(0, self._candle_idx - hist)
            end = self._candle_idx
            candle_view[sym] = [
                Candle(
                    timestamp=c["timestamp"],
                    open=c["open"], high=c["high"],
                    low=c["low"], close=c["close"],
                    volume=c["volume"],
                )
                for c in raw[start:end]
            ]

        return TradingObservation(
            step=self._step,
            max_steps=int(cfg["max_steps"]),
            task_id=self._task_id,
            candle_index=self._candle_idx,
            instruments=self._instruments,
            candles=candle_view,
            portfolio=self._portfolio,
            last_action_result=self._last_result,
            reward=reward,
            done=self._done,
            info={
                "total_margin_deployed": self._total_margin_deployed,
                "open_positions": len(self._portfolio.positions),
                "closed_positions": len(self._portfolio.closed_positions),
            },
        )

    def get_state(self) -> TradingObservation:
        if self._portfolio is None:
            raise RuntimeError("Environment not initialised. Call reset() first.")
        return self._build_observation(reward=0.0)

    @property
    def is_done(self) -> bool:
        return self._done


def _synthetic_candles(base_price: float, n: int) -> List[dict]:
    import random
    candles = []
    price = base_price
    for i in range(n):
        change = price * random.uniform(-0.01, 0.01)
        o = price
        c = price + change
        h = max(o, c) * 1.002
        l = min(o, c) * 0.998
        candles.append({
            "timestamp": f"2025-01-{i+1:02d}",
            "open": round(o, 2), "high": round(h, 2),
            "low": round(l, 2), "close": round(c, 2),
            "volume": 1000.0,
        })
        price = c
    return candles
