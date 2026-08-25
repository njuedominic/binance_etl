from datetime import datetime, timezone
import pandas as pd

def transform_data(raw_data:dict) -> pd.DataFrame:
    """
    Transform the raw data into a pandas DataFrame.

    Args:
        raw_data (dict): The raw data dictionary containing 'symbol' and 'price'.

    Returns:
        pd.DataFrame: A DataFrame with columns 'symbol', 'price', and 'timestamp'.
    """
    try:
        if not raw_data.get("success", True):
            return pd.DataFrame()

        return pd.DataFrame(
            [{
                "symbol": str(raw_data["symbol"]),
                "price": float(raw_data["price"]),
                "extracted_at": datetime.now(timezone.utc),
            }]
        )

    except (KeyError, TypeError, ValueError):
        return pd.DataFrame()