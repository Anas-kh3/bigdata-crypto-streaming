# InfluxDB Schema

Bucket: `crypto`
Org: `bigdata`

## Measurement: crypto_latest
Tags:
- source (binance / coingecko)
- symbol (btc / eth)

Fields:
- price (float)
- volume_24h (float)

Time:
- max(time) per group

## Measurement: crypto_1min
Tags:
- source
- symbol

Fields:
- avg_price (float)
- sum_volume_24h (float)

Time:
- window start (1 min)
