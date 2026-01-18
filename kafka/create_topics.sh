#!/usr/bin/env bash
set -e

TOPIC="crypto_ticks"
BOOTSTRAP="${KAFKA_BOOTSTRAP:-master:9092}"

echo "[Kafka] Creating topic ${TOPIC} on ${BOOTSTRAP}"

kafka-topics.sh --bootstrap-server "$BOOTSTRAP" \
  --create --if-not-exists \
  --topic "$TOPIC" \
  --partitions 3 --replication-factor 1

echo "[Kafka] Topics list:"
kafka-topics.sh --bootstrap-server "$BOOTSTRAP" --list
