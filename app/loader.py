import os
import json
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

def load_table(data: list[dict]):
    if len(data) == 1:
        row = data[0]
        print("\n--------------------------------------------------")
        print("BINANCE CRYPTO PRICE")
        print("--------------------------------------------------")
        print(f"Symbol:            {row['symbol']}")
        print(f"Price USDT:        ${row['price_usdt']:,.2f}")
        print(f"USD/KES Rate:      {row['usd_kes_rate']:.2f}")
        print(f"Approx. Price in KES: KSh {row['price_kes']:,.2f}")
        print("--------------------------------------------------")
        print(f"Source: {row['source'].capitalize()}")
        print(f"Status: {row['status'].upper()}")
        print("--------------------------------------------------")
    else:
        print("\n---------------------------------------------------------------")
        print(f"{'SYMBOL':<14}{'USDT PRICE':<23}{'APPROXIMATE KES':<20}")
        print("---------------------------------------------------------------")
        for row in data:
            print(f"{row['symbol']:<14}${row['price_usdt']:<22,.2f}KSh {row['price_kes']:<18,.2f}")
        print("---------------------------------------------------------------")

def load_json(data: list[dict]):
    output = data[0] if len(data) == 1 else data
    print(json.dumps(output, indent=4))

def load_csv(data: list[dict]):
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    csv_path = "data/output.csv"
    df.to_csv(csv_path, index=False)
    print(f"[LOAD] Data successfully written to {csv_path}")

def load_postgres(data: list[dict]):
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "crypto")
    user = os.getenv("POSTGRES_USER", "dom")
    password = os.getenv("POSTGRES_PASSWORD")
    
    if not password:
        print("ERROR: POSTGRES_PASSWORD environment variable is required.")
        return

    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(db_url)
    
    df = pd.DataFrame(data)[["symbol", "price_usdt", "usd_kes_rate", "price_kes", "extracted_at"]]
    df.to_sql("crypto_prices", engine, if_exists="append", index=False)
    print("[LOAD] Data successfully inserted into PostgreSQL database.")

def output_data(data: list[dict], fmt: str):
    if fmt == "json":
        load_json(data)
    elif fmt == "csv":
        load_csv(data)
    elif fmt == "postgres":
        load_postgres(data)
    else:
        load_table(data)