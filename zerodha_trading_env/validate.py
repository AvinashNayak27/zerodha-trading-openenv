"""
validate.py -- End-to-end validation suite for the Zerodha Trading Environment.
"""

from __future__ import annotations

import argparse
import sys
import traceback
from typing import Any, Dict, List, Tuple


def validate_direct() -> List[Tuple[str, bool, str]]:
    from zerodha_trading_env.environment import ZerodhaTradingEnv
    from zerodha_trading_env.models import TradingAction, ActionType, OrderSide, Segment
    from zerodha_trading_env.graders import task1_grader, task2_grader, task3_grader

    results = []

    for task_id, grader in [
        ("task_1_single_trade", task1_grader),
        ("task_2_portfolio", task2_grader),
        ("task_3_full_session", task3_grader),
    ]:
        try:
            env = ZerodhaTradingEnv()
            obs = env.reset(task_id)
            assert not obs.done
            while not obs.done:
                obs = env.step(TradingAction(action_type=ActionType.HOLD))
            grade = grader.grade(obs)
            assert "score" in grade
            results.append((f"{task_id} (direct)", True, f"Score={grade['score']:.4f} | {grade['summary']}"))
        except Exception:
            results.append((f"{task_id} (direct)", False, traceback.format_exc()))

    try:
        from zerodha_trading_env.data.instruments import ALL_SYMBOLS, EQ_SYMBOLS, FO_SYMBOLS, COM_SYMBOLS
        assert len(ALL_SYMBOLS) == 72
        results.append(("instrument_registry", True, f"72 instruments OK"))
    except Exception:
        results.append(("instrument_registry", False, traceback.format_exc()))

    return results


def validate_http(base_url: str) -> List[Tuple[str, bool, str]]:
    try:
        import httpx
    except ImportError:
        return [("http_import", False, "httpx not installed")]

    results = []
    client = httpx.Client(base_url=base_url, timeout=60.0)

    try:
        r = client.get("/health")
        r.raise_for_status()
        data = r.json()
        assert data["status"] == "ok"
        results.append(("GET /health", True, f"version={data.get('version')}"))
    except Exception as exc:
        results.append(("GET /health", False, str(exc)))
        return results

    for task_id in ["task_1_single_trade", "task_2_portfolio", "task_3_full_session"]:
        try:
            r = client.post("/reset", json={"task_id": task_id})
            r.raise_for_status()
            obs = r.json()
            step_count = 0
            while not obs["done"]:
                r = client.post("/step", json={"action": {"action_type": "HOLD"}})
                r.raise_for_status()
                obs = r.json()
                step_count += 1
                if step_count > 200:
                    break
            cap = obs["portfolio"]["capital"]
            results.append((f"POST /reset+step ({task_id})", True, f"steps={step_count} capital={cap:.0f}"))
        except Exception:
            results.append((f"POST /reset+step ({task_id})", False, traceback.format_exc()))

    return results


def print_report(results: List[Tuple[str, bool, str]]) -> int:
    print("\n" + "=" * 70)
    print("  ZERODHA TRADING ENV -- VALIDATION REPORT")
    print("=" * 70)
    failures = 0
    for name, passed, msg in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
        if not passed:
            failures += 1
            for line in msg.strip().splitlines()[-5:]:
                print(f"         {line}")
        else:
            print(f"         {msg[:80]}")
    print("=" * 70)
    total = len(results)
    print(f"  Result: {total - failures}/{total} passed")
    print("=" * 70 + "\n")
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:7860")
    parser.add_argument("--direct", action="store_true")
    args = parser.parse_args()
    results = validate_direct() if args.direct else validate_http(args.base_url)
    failures = print_report(results)
    sys.exit(1 if failures > 0 else 0)


if __name__ == "__main__":
    main()
