import os
from dotenv import load_dotenv

load_dotenv()

def env(name: str, default: str = "") -> str:
    v = os.getenv(name, default)
    if v is None:
        return default
    return v
