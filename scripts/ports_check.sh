#!/usr/bin/env bash
echo "Kafka (9092):"
nc -vz master 9092 || true

echo "InfluxDB (8086):"
nc -vz localhost 8086 || true

echo "Grafana (3001 or 3000):"
nc -vz localhost 3001 || nc -vz localhost 3000 || true
