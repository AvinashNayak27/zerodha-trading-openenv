"""
Grader for task_1_single_trade.
Score = (realized_pnl / margin_used) * modifier
"""

from __future__ import annotations
from typing import Dict, Any
from zerodha_trading_env.models import TradingObservation, PositionStatus


def grade(final_obs: TradingObservation) -> Dict[str, Any]:
    portfolio = final_obs.portfolio
    closed = portfolio.closed_positions

    if not closed:
        return {"score": 0.0, "breakdown": {"realized_pnl": 0.0, "margin_used": 0.0}, "summary": "No trade opened. Score: 0.0"}

    pos = closed[0]
    margin_used = pos.margin_used if pos.margin_used > 0 else 1.0
    efficiency = pos.realized_pnl / margin_used

    modifier = 1.0
    if pos.status == PositionStatus.TARGET_HIT:
        modifier = 1.20
    elif pos.status == PositionStatus.SL_HIT:
        modifier = 0.80

    score = efficiency * modifier
    breakdown = {
        "realized_pnl": round(pos.realized_pnl, 2),
        "margin_used": round(margin_used, 2),
        "capital_efficiency": round(efficiency, 6),
        "exit_type": pos.status.value,
        "modifier": modifier,
    }
    summary = (f"Task 1 | P&L: {pos.realized_pnl:+.0f} | Margin: {margin_used:.0f} | "
               f"Efficiency: {efficiency:.4f} | Exit: {pos.status.value} | Score: {score:.4f}")
    return {"score": round(score, 6), "breakdown": breakdown, "summary": summary}
