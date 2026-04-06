"""
FastAPI server exposing the Zerodha Trading Environment over HTTP.

Endpoints:
  POST /reset       - start a new episode
  POST /step        - submit one action, advance one candle
  GET  /state       - get current observation without advancing
  GET  /health      - liveness check
  GET  /tasks       - list all available tasks
  GET  /instruments - list all 72 instruments
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from zerodha_trading_env.environment import ZerodhaTradingEnv, TASK_CONFIGS
from zerodha_trading_env.models import TradingAction, TradingObservation
from zerodha_trading_env.data.instruments import INSTRUMENTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zerodha Trading Environment",
    description="OpenEnv-compatible historical replay environment for trading agents.",
    version="0.1.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_env = ZerodhaTradingEnv()


class ResetRequest(BaseModel):
    task_id: str = "task_1_single_trade"
    config: Optional[Dict[str, Any]] = None


class StepRequest(BaseModel):
    action: TradingAction


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/health", response_model=HealthResponse, tags=["Meta"])
def health():
    return HealthResponse(status="ok", version="0.1.0")


@app.get("/tasks", tags=["Meta"])
def list_tasks():
    tasks = []
    for task_id, cfg in TASK_CONFIGS.items():
        tasks.append({
            "id": task_id,
            "name": cfg["name"],
            "difficulty": cfg["difficulty"],
            "max_steps": cfg["max_steps"],
            "initial_capital": cfg["initial_capital"],
            "n_instruments": len(cfg["instruments"]),
            "max_positions": cfg.get("max_positions", 10),
        })
    return {"tasks": tasks}


@app.get("/instruments", tags=["Meta"])
def list_instruments(segment: Optional[str] = None):
    data = []
    for sym, info in INSTRUMENTS.items():
        if segment and info["segment"] != segment.upper():
            continue
        data.append({"symbol": sym, "segment": info["segment"], "yf_ticker": info["yf_ticker"],
                     "lot_size": info["lot_size"], "margin_pct": info["margin_pct"], "description": info["description"]})
    return {"count": len(data), "instruments": data}


@app.post("/reset", response_model=TradingObservation, tags=["Environment"])
def reset(request: ResetRequest):
    try:
        obs = _env.reset(task_id=request.task_id, config=request.config)
        return obs
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Reset error")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/step", response_model=TradingObservation, tags=["Environment"])
def step(request: StepRequest):
    try:
        obs = _env.step(request.action)
        return obs
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Step error")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/state", response_model=TradingObservation, tags=["Environment"])
def get_state():
    try:
        return _env.get_state()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("State error")
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("zerodha_trading_env.server.app:app", host="0.0.0.0", port=port, reload=False)
