# Grafana Flux Queries

## 1) BTC vs ETH (avg price 1min)
```flux
from(bucket: "crypto")
  |> range(start: -6h)
  |> filter(fn: (r) => r._measurement == "crypto_1min")
  |> filter(fn: (r) => r._field == "avg_price")
  |> filter(fn: (r) => r.symbol == "btc" or r.symbol == "eth")
