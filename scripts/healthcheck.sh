#!/usr/bin/env bash
set -e

echo "[Influx] ping..."
curl -s http://localhost:8086/health | head -c 200; echo ""

echo "[Grafana] ping..."
curl -s http://localhost:3001/api/health | head -c 200 || true
echo ""
