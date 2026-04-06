"""
Grader for task_3_full_session.
Score = capital_efficiency * drawdown_penalty * volatility_penalty * segment_bonus
"""

from __future__ import annotations
from typing import Dict, Any
import math
from zerodha_trading_env.models import TradingObservation


def grade(final_obs: TradingObservation) -> Dict[str, Any]:
    portfolio = final_obs.portfolio
    closed = portfolio.closed_positions
    info = final_obs.info

    total_realized = portfolio.realized_pnl
    total_margin = max(info.get("total_margin_deployed", 1.0), 1.0)
    max_drawdown = portfolio.max_drawdown
    total_trades = portfolio.total_trades
    winning_trades = portfolio.winning_trades

    cap_efficiency = total_realized / total_margin
    drawdown_penalty = max(0.3, 1.0 - 3.0 * max_drawdown)

    pnl_values = [p.realized_pnl for p in closed] if closed else [0.0]
    mean_pnl = sum(pnl_values) / len(pnl_values)
    variance = sum((x - mean_pnl) ** 2 for x in pnl_values) / len(pnl_values)
    pnl_std = math.sqrt(variance)
    denom = max(abs(mean_pnl), 1.0)
    volatility_penalty = max(0.7, 1.0 - pnl_std / denom)

    segments_traded = {p.segment.value for p in closed} if closed else set()
    segment_bonus = 1.0 + 0.05 * len(segments_traded)

    score = cap_efficiency * drawdown_penalty * volatility_penalty * segment_bonus
    win_rate = (winning_trades / total_trades) if total_trades > 0 else 0.0
    unique_instruments = len({p.instrument for p in closed}) if closed else 0

    breakdown = {
        "total_realized_pnl": round(total_realized, 2),
        "total_margin_deployed": round(total_margin, 2),
        "capital_efficiency": round(cap_efficiency, 6),
        "max_drawdown": round(max_drawdown, 4),
        "drawdown_penalty": round(drawdown_penalty, 4),
        "pnl_std": round(pnl_std, 2),
        "volatility_penalty": round(volatility_penalty, 4),
        "segments_traded": list(segments_traded),
        "segment_bonus": round(segment_bonus, 4),
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "win_rate": round(win_rate, 4),
        "unique_instruments": unique_instruments,
    }
    summary = (f"Task 3 | P&L: {total_realized:+.0f} | Margin: {total_margin:.0f} | "
               f"Eff: {cap_efficiency:.4f} | DD: {max_drawdown:.2%} | Score: {score:.4f}")
    return {"score": round(score, 6), "breakdown": breakdown, "summary": summary}
