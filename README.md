# Big Data Streaming Project — Real-Time Cryptocurrency Monitoring

This project aims to build an end-to-end Big Data pipeline to monitor real-time cryptocurrency 
prices (Bitcoin, Ethereum, etc.) using:

- Apache Kafka (data ingestion)
- Apache Spark (Structured Streaming processing)
- HDFS (raw data storage)
- InfluxDB (time-series database)
- Grafana (real-time dashboards)

## Data Sources
- CoinGecko API (no key required)
- Binance Public API (no key required)

## Architecture (High-Level)
Kafka → HDFS → Spark → InfluxDB → Grafana

## Repository Structure
- `producers/` — Kafka producers for fetching crypto data
- `spark/` — Spark jobs for streaming processing
- `grafana/` — dashboard templates and instructions
- `hdfs/` — HDFS raw data folder (empty placeholder)
- `docs/` — project documentation (Checkpoint 1 PDF)

## Team Members
- Anas Khalil  
- Mourad Mahmoudi  
