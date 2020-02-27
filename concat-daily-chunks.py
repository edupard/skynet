import utils.gcs as gcs
import pandas as pd
import sys
from utils.batch_utils import get_worker_batch

gcs_client = gcs.GcsClient()
gcs_client.get('tiingo/stocks/SPY.csv', '/tmp/SPY.csv')
spy_df = pd.read_csv('/tmp/SPY.csv')

worker_idx = int(sys.argv[1])
num_workers = int(sys.argv[2])
dates = get_worker_batch(worker_idx, num_workers, spy_df.date.values)

for date in dates:
    dfs = []
    for b in range(75):
        rfp = f'tiingo/daily-chunks/{date}_{b}.csv'
        lfp = f'/tmp/{date}_{b}.csv'
        if gcs_client.get(rfp, lfp):
            df = pd.read_csv(lfp)
            dfs.append(df)
    df = pd.concat(dfs, axis=0)
    lfp = f'/tmp/{date}.csv'
    rfp = f'tiingo/daily/{date}.csv'
    df.to_csv(lfp, index=False)
    gcs_client.save(lfp, rfp)
