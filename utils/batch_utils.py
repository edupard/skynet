import os
import utils.gcs as gcs
import pandas as pd

def get_worker_tickers(worker_idx, num_workers):
    if not os.path.exists('/tmp/tickers.csv'):
        gcs_client = gcs.GcsClient()
        gcs_client.get('tiingo/tickers.csv', '/tmp/tickers.csv')
    df = pd.read_csv('/tmp/tickers.csv')
    tickers = df.ticker.values
    total = len(tickers)
    batch_size = (total // num_workers) + 1
    start = worker_idx * batch_size
    stop = start + batch_size
    tickers_to_process = tickers[start: stop]
    return tickers_to_process