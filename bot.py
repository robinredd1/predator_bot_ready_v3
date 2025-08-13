# bot.py — Minimal ready-to-run (Paper only)
# - Healthcheck keeps Repl alive until keys are accepted
# - Prints market session status every 5s (hook point for trading logic)

import sys, subprocess
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

import time
from datetime import datetime
from zoneinfo import ZoneInfo

from config import HEADERS, TRADING_BASE

def get(endpoint):
    return requests.get(f"{TRADING_BASE}{endpoint}", headers=HEADERS, timeout=15)

def healthcheck():
    while True:
        a = get("/v2/account")
        c = get("/v2/clock")
        print(f"🔑 Account={a.status_code} Clock={c.status_code}")
        if a.ok and c.ok:
            print("✅ Keys OK, connected to Alpaca Paper API."); return
        elif a.status_code in (401,403) or c.status_code in (401,403):
            print("❌ Auth rejected (401/403). Make sure these are TRADING API → PAPER keys.")
        else:
            print("⚠️ Unexpected response. Retrying…")
        time.sleep(15)

def loop():
    while True:
        try:
            c = get("/v2/clock").json()
            now_et = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S ET")
            print(f"⏱ {now_et} | is_open={c.get('is_open')} | next_open={c.get('next_open')} | next_close={c.get('next_close')}")
        except Exception as e:
            print("Loop error:", e)
        time.sleep(5)

if __name__ == "__main__":
    print("🚀 Predator minimal runner (paper only)")
    healthcheck()
    loop()
