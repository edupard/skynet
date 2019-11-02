from tiingo import TiingoClient
import os

def get_tiingo_client() -> TiingoClient:
    config = {}
    config['session'] = True
    config['api_key'] = os.environ['TIINGO_API_KEY']
    return TiingoClient(config)

def get_tiingo_tickers():
    client = get_tiingo_client()
    client.list_stock_tickers()
    tickers = client.list_stock_tickers()
    matches = [el for el in tickers if
               (el['exchange'] == "NASDAQ" or el['exchange'] == "NYSE") and el['assetType'] == 'Stock']
    return matches.append('SPY')

def get_tickers():
    get_tiingo_tickers()