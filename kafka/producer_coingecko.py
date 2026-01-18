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

# CoinGecko uses ids
ID_MAP = {"btc": "bitcoin", "eth": "ethereum"}

URL = "https://api.coingecko.com/api/v3/simple/price"

def fetch_coingecko(symbols):
    ids = ",".join(ID_MAP[s] for s in symbols if s in ID_MAP)
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_vol": "true"}
    r = requests.get(URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def main():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP)
    print(f"[CoinGecko] producing to {TOPIC} on {BOOTSTRAP}, symbols={SYMBOLS}")

    while True:
        try:
            data = fetch_coingecko(SYMBOLS)
            for sym in SYMBOLS:
                cid = ID_MAP.get(sym)
                if not cid or cid not in data:
                    continue
                price = data[cid].get("usd", None)
                vol = data[cid].get("usd_24h_vol", 0.0)
                if price is None:
                    continue
                ev = to_event("coingecko", sym, price, vol)
                producer.send(TOPIC, value=dumps_event(ev), key=sym.encode("utf-8"))
            producer.flush()
        except Exception as e:
            print("[CoinGecko] error:", str(e))
        sleep_s(POLL_SECONDS)

if __name__ == "__main__":
    main()

