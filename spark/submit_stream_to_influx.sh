#!/usr/bin/env bash
set -e

if [ ! -f ".env" ]; then
  echo "Missing .env file. Run: cp .env.example .env"
  exit 1
fi
source .env

# InfluxDB Spark connector (InfluxData)
# NOTE: If your Spark version differs, we adjust package version.
INFLUX_SPARK_PACKAGE="com.influxdb:influxdb-spark:2.0.0"

spark-submit \
  --packages "$INFLUX_SPARK_PACKAGE,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1" \
  spark/stream_kafka_to_influx.py
