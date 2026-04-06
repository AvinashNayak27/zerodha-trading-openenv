"""
inference.py -- Reference agent for the Zerodha Trading Environment HTTP API.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from typing import Any, Dict, Optional

import httpx

DEFAULT_BASE_URL = "http://localhost:7860"


def strategy_random(obs: Dict) -> Dict:
    portfolio = obs["portfolio"]
    open_pos = portfolio["positions"]
    instruments = obs["instruments"]
    action_type = random.choice(["HOLD", "HOLD", "OPEN", "CLOSE"])
    if action_type == "CLOSE" and open_pos:
        pos_id = random.choice(list(open_pos.keys()))
        return {"action_type": "CLOSE", "position_id": pos_id}
    if action_type == "OPEN" and instruments:
        instrument = random.choice(instruments)
        return {
            "action_type": "OPEN",
            "instrument": instrument,
            "segment": _infer_segment(instrument),
            "side": random.choice(["BUY", "SELL"]),
            "quantity": 1,
        }
    return {"action_type": "HOLD"}


def strategy_momentum(obs: Dict) -> Dict:
    portfolio = obs["portfolio"]
    open_pos = portfolio["positions"]
    instruments = obs["instruments"]
    candles = obs.get("candles", {})

    for pos_id, pos in open_pos.items():
        upnl = pos.get("unrealized_pnl", 0)
        margin = pos.get("margin_used", 1)
        if margin > 0 and upnl / margin < -0.01:
            return {"action_type": "CLOSE", "position_id": pos_id}

    if not open_pos and instruments:
        instrument = instruments[0]
        inst_candles = candles.get(instrument, [])
        if len(inst_candles) >= 2:
            last = inst_candles[-1]
            side = "BUY" if last["close"] > last["open"] else "SELL"
            sl_offset = last["close"] * 0.01
            tgt_offset = last["close"] * 0.02
            stoploss = last["close"] - sl_offset if side == "BUY" else last["close"] + sl_offset
            target = last["close"] + tgt_offset if side == "BUY" else last["close"] - tgt_offset
            return {
                "action_type": "OPEN",
                "instrument": instrument,
                "segment": _infer_segment(instrument),
                "side": side,
                "quantity": 1,
                "stoploss": round(stoploss, 2),
                "target": round(target, 2),
            }
    return {"action_type": "HOLD"}


STRATEGIES = {"random": strategy_random, "momentum": strategy_momentum}


def _infer_segment(symbol: str) -> str:
    com_tickers = {"GOLD", "SILVER", "COPPER", "ALUMINIUM", "CRUDEOIL", "NATURALGAS", "ZINC", "LEAD"}
    fo_suffixes = {"FUT", "CE", "PE"}
    upper = symbol.upper()
    for t in com_tickers:
        if upper.startswith(t):
            return "COM"
    for s in fo_suffixes:
        if upper.endswith(s):
            return "FO"
    return "EQ"


def run_episode(task_id: str = "task_1_single_trade", strategy: str = "momentum",
               base_url: str = DEFAULT_BASE_URL, max_steps: Optional[int] = None,
               verbose: bool = True) -> Dict[str, Any]:
    client = httpx.Client(base_url=base_url, timeout=30.0)
    strategy_fn = STRATEGIES.get(strategy, strategy_random)

    reset_payload: Dict[str, Any] = {"task_id": task_id}
    if max_steps:
        reset_payload["config"] = {"max_steps": max_steps}

    resp = client.post("/reset", json=reset_payload)
    resp.raise_for_status()
    obs = resp.json()

    step_count = 0
    total_reward = 0.0

    while not obs.get("done", False):
        action = strategy_fn(obs)
        resp = client.post("/step", json={"action": action})
        resp.raise_for_status()
        obs = resp.json()
        step_count += 1
        total_reward += obs.get("reward", 0.0)
        if max_steps and step_count >= max_steps:
            break

    portfolio = obs["portfolio"]
    return {
        "task_id": task_id,
        "strategy": strategy,
        "steps": step_count,
        "total_reward": round(total_reward, 6),
        "final_capital": round(portfolio["capital"], 2),
        "realized_pnl": round(portfolio["realized_pnl"], 2),
        "max_drawdown": round(portfolio["max_drawdown"], 4),
        "total_trades": portfolio["total_trades"],
        "winning_trades": portfolio["winning_trades"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default="task_1_single_trade")
    parser.add_argument("--strategy", default="momentum", choices=list(STRATEGIES))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--steps", type=int, default=None)
    args = parser.parse_args()
    result = run_episode(task_id=args.task, strategy=args.strategy,
                         base_url=args.base_url, max_steps=args.steps)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
