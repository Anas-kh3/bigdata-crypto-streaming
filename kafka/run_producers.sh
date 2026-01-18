#!/usr/bin/env bash
set -e

if [ ! -f ".env" ]; then
  echo "Missing .env file. Run: cp .env.example .env"
  exit 1
fi

source .env

python3 -m venv .venv || true
source .venv/bin/activate
pip install -r requirements.txt

echo "Starting producers..."
nohup python kafka/producer_coingecko.py > coingecko.log 2>&1 &
nohup python kafka/producer_binance.py > binance.log 2>&1 &

echo "Producers started. Logs: coingecko.log, binance.log"
