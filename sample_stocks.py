import pandas as pd
import utils.gcs as gcs
import numpy as np
import os
import sys
from utils.batch_utils import get_worker_batch

worker_idx = int(sys.argv[1])
num_workers = int(sys.argv[2])

gcs_client = gcs.GcsClient()

# get spy data
gcs_client.get("tiingo/stocks/SPY.csv", '/tmp/SPY.csv')
spy_df = pd.read_csv('/tmp/SPY.csv')

gcs_client.get("tiingo/tickers.csv", '/tmp/tickers.csv')
tickers_df = pd.read_csv('/tmp/tickers.csv')

num_tickers = len(tickers_df.ticker.values)

gv = np.zeros((num_tickers, 64), dtype=np.float)
c = np.zeros((num_tickers), dtype=np.float)

ticker_idx_dict = {}
for index, row in tickers_df.iterrows():
    ticker_idx_dict[row.ticker] = index

def get_idx_by_ticker(ticker):
    return ticker_idx_dict[ticker]

def get_ticker_by_idx(idx):
    return tickers_df.iloc[idx].ticker

os.makedirs('/tmp/daily', exist_ok=True)

i_spy_dates = spy_df.date.values.astype(np.int)
i = 0
i_dates = get_worker_batch(worker_idx, num_workers, i_spy_dates, lag = 63)
for i_date in i_dates:
    i = i + 1

    gv = np.roll(gv, -1, axis = 1)
    gv[:,-1] = 0

    c[:] = 0

    gcs_client.get(f'tiingo/daily/{i_date}.csv', f'/tmp/daily/{i_date}.csv')
    daily_df = pd.read_csv(f'/tmp/daily/{i_date}.csv')

    idx_arr = np.array(list(map(lambda t: get_idx_by_ticker(t), daily_df.ticker.values)), dtype = np.int)
    gv[idx_arr,-1] = daily_df.v.values * (daily_df.h.values + daily_df.l.values + daily_df.c.values) / 3
    c[idx_arr] = daily_df.c

    # not enough data
    if i < 64:
        continue

    gv_avg = np.average(gv, axis=1)
    idx_by_avg_gv_asc = np.argsort(gv_avg)
    idx_by_avg_gv_desc = idx_by_avg_gv_asc[::-1]

    selection = []
    for idx in idx_by_avg_gv_desc:
        ticker = get_ticker_by_idx(idx)
        if ticker == 'SPY' or ticker == 'ZXZZT' or ticker == '0001753539':
            continue
        # do not trade warrants & preferred stocks
        if "-P" in ticker or "-W" in ticker:
            continue
        # do not trade pink sheets
        if c[idx] < 5.0:
            continue
        # should be always traded before
        if np.all(gv[idx, :] > 0):
            if ticker not in selection:
                selection.append(ticker)
        if len(selection) == 500:
            break

    lfp = f'/tmp/{i_date}.csv'
    rfp = f'tiingo/stock_samples/{i_date}.csv'
    pd.DataFrame({'ticker': selection}).to_csv(lfp, index=False)
    gcs_client.save(lfp, rfp)


