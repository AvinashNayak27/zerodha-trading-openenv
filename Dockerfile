FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY zerodha_trading_env/ ./zerodha_trading_env/
COPY openenv.yaml ./openenv.yaml

# HuggingFace Spaces uses port 7860
EXPOSE 7860
ENV PORT=7860
ENV PYTHONPATH=/app

CMD ["python", "-m", "uvicorn", "zerodha_trading_env.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
