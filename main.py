import argparse
from app.extract import extract_data
from app.transform import transform_data
from app.loader import output_data

def main():
    parser = argparse.ArgumentParser(description="Binance Crypto Price ETL")
    parser.add_argument("--symbol", type=str, required=True, help="Binance trading pair (e.g. BTCUSDT or BTCUSDT,ETHUSDT)")
    parser.add_argument("--output", type=str, choices=["table", "json", "csv", "postgres"], default="table")
    
    args = parser.parse_args()
    symbols = [s.strip() for s in args.symbol.split(",") if s.strip()]
    
    prices, rate = extract_data(symbols)
    transformed_data = transform_data(prices, rate)
    output_data(transformed_data, args.output)

if __name__ == "__main__":
    main()