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

stock_traded_mask = np.zeros((num_tickers, 64), dtype=np.bool)

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

    stock_traded_mask = np.roll(stock_traded_mask, -1, axis=1)
    stock_traded_mask[:, -1] = False

    gcs_client.get(f'tiingo/daily/{i_date}.csv', f'/tmp/daily/{i_date}.csv')
    daily_df = pd.read_csv(f'/tmp/daily/{i_date}.csv')
    daily_df['gv'] = daily_df.v.values * (daily_df.h.values + daily_df.l.values + daily_df.c.values) / 3
    daily_df = daily_df.sort_values(by=['gv'], ascending=False)

    for index, row in daily_df.iterrows():
        if row.v > 0:
            stock_traded_mask[get_idx_by_ticker(row.ticker), -1] = True

    # not enought data
    if i < 64:
        continue

    selection = []
    for index, row in daily_df.iterrows():
        ticker = row.ticker
        if ticker == 'SPY' or ticker == 'ZXZZT':
            continue
        if np.all(stock_traded_mask[get_idx_by_ticker(ticker), :]):
            selection.append(ticker)
        if len(selection) == 500:
            break

    lfp = f'/tmp/{i_date}.csv'
    rfp = f'tiingo/sample_stocks/{i_date}.csv'
    pd.DataFrame({'ticker': selection}).to_csv(lfp, index=False)
    gcs_client.save(lfp, rfp)


