from utils.batch_utils import get_worker_batch
import sys
import utils.gcs as gcs
import pandas as pd

worker_idx = int(sys.argv[1])
num_workers = int(sys.argv[2])

gcs_client = gcs.GcsClient()
gcs_client.get('tiingo/tickers.csv', '/tmp/tickers.csv')
df = pd.read_csv('/tmp/tickers.csv')
tickers = get_worker_batch(worker_idx, num_workers, df.ticker.values)

daily_data = {}

for ticker in tickers:
    if not gcs_client.get(f'tiingo/stocks/{ticker}.csv', f'/tmp/{ticker}.csv'):
        continue

    # process ticker
    df = pd.read_csv(f'/tmp/{ticker}.csv')
    df['ticker'] = ticker

    for index, row in df.iterrows():
        date = int(row.date)
        if date not in daily_data:
            daily_data[date] = []
        values = daily_data[date]
        values.append(row)

for date, dps in daily_data.items():
    df = pd.DataFrame(dps)
    df = df[["ticker", "o", "h", "l", "c", "v", "a_o", "a_h", "a_l", "a_c", "a_v", "div", "split"]]
    df.v = df.v.astype(int)
    df.a_v = df.a_v.astype(int)
    lfp = f"/tmp/{date}_{worker_idx}.csv"
    df.to_csv(lfp, index=False)
    gcs_client.save(lfp, f'tiingo/daily-chunks/{date}_{worker_idx}.csv')

