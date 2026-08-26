import sys
import requests

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
FRANKFURTER_URL = "https://api.frankfurter.dev/v2/rate/USD/KES"

def fetch_binance_price(symbol: str) -> float:
    try:
        response = requests.get(BINANCE_URL, params={"symbol": symbol.upper()}, timeout=10)
        if response.status_code == 400:
            print(f"ERROR: {symbol.upper()} is not a valid Binance trading pair.")
            sys.exit(1)
        response.raise_for_status()
        return float(response.json()["price"])
    except requests.exceptions.RequestException:
        print("ERROR: Unable to connect to Binance API.\nPlease check your internet connection.")
        sys.exit(1)

def fetch_usd_kes_rate() -> float:
    try:
        response = requests.get(FRANKFURTER_URL, timeout=10)
        response.raise_for_status()
        return response.json()["rate"]
    except requests.exceptions.RequestException:
        print("ERROR: Unable to retrieve the USD/KES exchange rate.")
        sys.exit(1)

def extract_data(symbols: list[str]) -> tuple[dict[str, float], float]:
    print("[EXTRACT] Fetching crypto prices from Binance...")
    prices = {symbol.upper(): fetch_binance_price(symbol) for symbol in symbols}
    print("[EXTRACT] Fetching USD/KES exchange rate...")
    rate = fetch_usd_kes_rate()
    return prices, rate