# Zerodha Trading Environment

An **OpenEnv-compatible** historical replay environment for training AI trading agents on real Zerodha instrument data across Equity, Futures & Options, and Commodity segments.

## Overview

| Property | Value |
|----------|-------|
| Instruments | 72 (10 EQ + 34 FO + 28 COM) |
| Data source | yfinance (OHLCV proxy) |
| Reward | Capital efficiency: P&L / margin used |
| Interface | HTTP REST API (FastAPI) |
| Port | 7860 (HuggingFace Spaces compatible) |

## Tasks

| Task ID | Name | Difficulty | Capital | Max Steps |
|---------|------|------------|---------|-----------|
| `task_1_single_trade` | Single Trade Efficiency | Easy | 5L | 20 |
| `task_2_portfolio` | Multi-Position Portfolio | Medium | 20L | 50 |
| `task_3_full_session` | Full Trading Session | Hard | 50L | 100 |

## Quick Start

### Install dependencies

```bash
pip install -r server/requirements.txt
```

### Run the server

```bash
python -m uvicorn zerodha_trading_env.server.app:app --host 0.0.0.0 --port 7860
```

### Run a baseline episode (momentum strategy)

```bash
python -m zerodha_trading_env.inference --task task_1_single_trade --strategy momentum
```

### Validate the environment

```bash
# Direct (no server needed)
python -m zerodha_trading_env.validate --direct

# Against live server
python -m zerodha_trading_env.validate --base-url http://localhost:7860
```

## API Reference

### `POST /reset`

Start a new episode.

```json
{
  "task_id": "task_1_single_trade",
  "config": {}
}
```

Returns: `TradingObservation`

### `POST /step`

Submit one action and advance one candle.

```json
{
  "action": {
    "action_type": "OPEN",
    "instrument": "GOLD26JUNFUT",
    "segment": "COM",
    "side": "BUY",
    "quantity": 1,
    "stoploss": 88000.0,
    "target": 92000.0
  }
}
```

Action types: `HOLD` | `OPEN` | `CLOSE` | `MODIFY` | `HEDGE`

Returns: `TradingObservation` (includes `reward`, `done`, `portfolio`)

### `GET /state`

Get current observation without stepping.

### `GET /health`

Liveness probe: `{"status": "ok", "version": "0.1.0"}`

### `GET /tasks`

List all task definitions.

### `GET /instruments?segment=COM`

List all 72 instruments, optionally filtered by segment.

## Project Structure

```
zerodha-trading-env/
├── openenv.yaml
├── pyproject.toml
├── Dockerfile
├── server/
│   └── requirements.txt
└── zerodha_trading_env/
    ├── environment.py
    ├── models.py
    ├── inference.py
    ├── validate.py
    ├── data/
    │   ├── instruments.py
    │   └── loader.py
    ├── graders/
    │   ├── task1_grader.py
    │   ├── task2_grader.py
    │   └── task3_grader.py
    └── server/
        └── app.py
```

## Scoring

### Task 1
```
score = (realized_pnl / margin_used) * modifier
modifier: TARGET_HIT=1.2x | SL_HIT=0.8x | manual=1.0x
```

### Task 2
```
score = capital_efficiency * drawdown_multiplier * diversity_bonus
```

### Task 3
```
score = capital_efficiency * drawdown_penalty * volatility_penalty * segment_bonus
```

## Author

Avinash Malothu -- MIT License
