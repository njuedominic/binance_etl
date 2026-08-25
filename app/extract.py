import requests

BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/price"

def extract_binance_price(symbol: str) -> dict:
    '''
    Fetch the latest ticker from Binance.

    Returns:
        dict: Binance response, e.g.
              {"symbol": "BTCUSDT", "price": "64250.12"}

    Raises:
        ValueError: For invalid symbols or malformed responses.
        RuntimeError: For network/API-related issues.

    '''
    try:
        response =requests.get(
            BINANCE_TICKER_URL,
            params={"symbol": symbol.upper()},
            timeout=20,
        )

        data = response.json()
        response.raise_for_status()

        if "price" not in data:
            return {
                "success": False,
                "error": data.get("msg", "Unknown error"),
            }
        return {
            "success": True,
            "symbol": data["symbol"],
            "price": float(data["price"]),
            "timestamp": data.get("time", None),
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
        }