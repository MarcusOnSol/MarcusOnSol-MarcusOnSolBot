
import requests
import sqlite3
import time
import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

CONFIG_PATH = "config.json"

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Config file {CONFIG_PATH} not found.")

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

MEMECOIN_BLACKLIST = set(CONFIG.get("blacklists", {}).get("memecoins", []))
DEV_BLACKLIST = set(CONFIG.get("blacklists", {}).get("devs", []))

DB_NAME = "coins_analysis.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS pumpfun_coins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin_name TEXT,
        symbol TEXT,
        migration_timestamp TEXT,
        raw_data TEXT,
        UNIQUE(coin_name, symbol)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS dexscreener_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token_address TEXT UNIQUE,
        coin_name TEXT,
        symbol TEXT,
        pair_age TEXT,
        hour_txns INTEGER,
        five_min_txns INTEGER,
        raw_data TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS gmgn_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token_address TEXT UNIQUE,
        holder_count INTEGER,
        top_holders_distribution TEXT,
        suspicious_connections INTEGER,
        twitter_rating TEXT,
        raw_data TEXT
    )""")
    conn.commit()
    conn.close()

def update_config_blacklists():
    CONFIG["blacklists"]["memecoins"] = list(MEMECOIN_BLACKLIST)
    CONFIG["blacklists"]["devs"] = list(DEV_BLACKLIST)
    with open(CONFIG_PATH, "w") as f:
        json.dump(CONFIG, f, indent=4)

def main():
    init_db()
    logging.info("Bot setup complete. Add your logic here.")

if __name__ == "__main__":
    main()
