"""
Grader for task_2_portfolio.
Score = capital_efficiency * drawdown_multiplier * diversity_bonus
"""

from __future__ import annotations
from typing import Dict, Any
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
    drawdown_mult = max(0.5, 1.0 - 2.0 * max_drawdown)
    unique_instruments = len({p.instrument for p in closed}) if closed else 0
    diversity_bonus = 1.0 + 0.10 * min(unique_instruments, 5) / 5.0
    score = cap_efficiency * drawdown_mult * diversity_bonus
    win_rate = (winning_trades / total_trades) if total_trades > 0 else 0.0

    breakdown = {
        "total_realized_pnl": round(total_realized, 2),
        "total_margin_deployed": round(total_margin, 2),
        "capital_efficiency": round(cap_efficiency, 6),
        "max_drawdown": round(max_drawdown, 4),
        "drawdown_multiplier": round(drawdown_mult, 4),
        "unique_instruments": unique_instruments,
        "diversity_bonus": round(diversity_bonus, 4),
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "win_rate": round(win_rate, 4),
    }
    summary = (f"Task 2 | P&L: {total_realized:+.0f} | Margin: {total_margin:.0f} | "
               f"Eff: {cap_efficiency:.4f} | DD: {max_drawdown:.2%} | Score: {score:.4f}")
    return {"score": round(score, 6), "breakdown": breakdown, "summary": summary}
