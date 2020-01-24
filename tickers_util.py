import sys
from abstractions.tiingo import TICKER_COLUMN, get_tickers

def get_tickers_chunk(num_workers):
    worker_idx = int(sys.argv[1])
    df = get_tickers()
    tickers = df[TICKER_COLUMN].values
    total = len(tickers)
    batch_size = (total // num_workers) + 1
    start = worker_idx * batch_size
    stop = start + batch_size
    tickers_to_process = tickers[start: stop]

    return worker_idx, tickers_to_process