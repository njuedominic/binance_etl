from datetime import datetime, timezone

def transform_data(prices: dict[str, float], rate: float) -> list[dict]:
    print("[TRANSFORM] Calculating approximate KES value...")
    transformed = []
    timestamp = datetime.now(timezone.utc).isoformat()
    for symbol, usdt_price in prices.items():
        transformed.append({
            "symbol": symbol,
            "price_usdt": usdt_price,
            "usd_kes_rate": rate,
            "price_kes": round(usdt_price * rate, 2),
            "source": "binance",
            "status": "success",
            "extracted_at": timestamp
        })
    return transformed