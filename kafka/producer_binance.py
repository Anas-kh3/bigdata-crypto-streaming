import os
import requests
from dotenv import load_dotenv
from kafka import KafkaProducer

from common import to_event, dumps_event, sleep_s

load_dotenv()

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "master:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "crypto_ticks")
SYMBOLS = [s.strip().lower() for s in os.getenv("SYMBOLS", "btc,eth").split(",")]
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "10"))

# Binance symbols
BINANCE_MAP = {"btc": "BTCUSDT", "eth": "ETHUSDT"}

TICKER_URL = "https://api.binance.com/api/v3/ticker/24hr"

def fetch_binance(sym_pair: str):
    r = requests.get(TICKER_URL, params={"symbol": sym_pair}, timeout=20)
    r.raise_for_status()
    return r.json()

def main():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP)
    print(f"[Binance] producing to {TOPIC} on {BOOTSTRAP}, symbols={SYMBOLS}")

    while True:
        try:
            for sym in SYMBOLS:
                pair = BINANCE_MAP.get(sym)
                if not pair:
                    continue
                data = fetch_binance(pair)
                price = float(data["lastPrice"])
                vol_quote = float(data.get("quoteVolume", 0.0))  # USDT volume (approx USD)
                ev = to_event("binance", sym, price, vol_quote)
                producer.send(TOPIC, value=dumps_event(ev), key=sym.encode("utf-8"))
            producer.flush()
        except Exception as e:
            print("[Binance] error:", str(e))
        sleep_s(POLL_SECONDS)

if __name__ == "__main__":
    main()
