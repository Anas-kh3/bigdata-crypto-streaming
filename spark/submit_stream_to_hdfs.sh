#!/usr/bin/env bash
set -e

if [ ! -f ".env" ]; then
  echo "Missing .env file. Run: cp .env.example .env"
  exit 1
fi
source .env

spark-submit \
  --packages "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1" \
  spark/stream_kafka_to_hdfs.py
