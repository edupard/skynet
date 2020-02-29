import utils.gcs as gcs
import numpy as np
from abstractions.log import log
from utils.batch_utils import get_worker_batch
import sys
import pandas as pd

worker_idx = int(sys.argv[1])
num_workers = int(sys.argv[2])

gcs_client = gcs.GcsClient()
gcs_client.get('tiingo/tickers.csv', '/tmp/tickers.csv')
df = pd.read_csv('/tmp/tickers.csv')
tickers = get_worker_batch(worker_idx, num_workers, df.ticker.values)

UP_TO_YEAR = 2008

lfp = f"/tmp/samples_up_to_{UP_TO_YEAR}.csv"
rfp = f"tiingo/samples_up_to_{UP_TO_YEAR}.csv"
gcs_client.get(rfp, lfp)
samples_df = pd.read_csv(lfp)

TS = 64
DIM = 12


def write_data(worker_idx, batch_data_dict):
    for batch_id, data in batch_data_dict.items():
        log(f"{worker_idx}: writing {batch_id} batch data")

        # get data to save
        idx, capacity, arr = data
        slice_to_save = arr[0:idx, :, :]

        # save np array
        lfp = f'/tmp/{batch_id}_{worker_idx}.npy'
        rfp = f'tiingo/batch_chunks/up_to_{UP_TO_YEAR}/{batch_id}_{worker_idx}.npy'
        np.save(lfp, slice_to_save)

        gcs_client.save(lfp, rfp)


def collect_data(ticker, batch_data_dict, df):
    data = df.to_numpy()
    dates_dict = {}
    idx = 0
    for date in data[:, 0]:
        iDate = int(date)
        dates_dict[iDate] = idx
        idx = idx + 1

    samples = samples_df.loc[samples_df.ticker == ticker]

    for idx, row in samples.iterrows():
        batch_id = row.batchId
        date = row.date
        if date not in dates_dict:
            continue
        end_idx = dates_dict[date]
        if end_idx < (TS - 1):
            continue
        sample_data = data[end_idx - (TS - 1): end_idx + 1, :]

        # https://github.com/philipperemy/keras-tcn#input-shape
        # (batch_size, timesteps, input_dim)
        if batch_id not in batch_data_dict:
            # allocate array
            batch_data_dict[batch_id] = (0, 100, np.zeros((100, TS, DIM)))

        idx, capacity, arr = batch_data_dict[batch_id]
        if idx == capacity:
            # double the capacity
            capacity = capacity * 2
            new_arr = np.zeros((capacity, TS, DIM))
            new_arr[0: idx, :, :] = arr
            arr = new_arr
        arr[idx, :, :] = sample_data
        idx = idx + 1
        batch_data_dict[batch_id] = (idx, capacity, arr)


batch_data_dict = {}

ticker_idx = 0
for ticker in tickers:
    ticker_idx = ticker_idx + 1
    log(f"{worker_idx}: processing {ticker} #{ticker_idx}")
    lfp = f"/tmp/{ticker}.csv"
    rfp = f'tiingo/preprocessed/{ticker}.csv'
    if not gcs_client.get(rfp, lfp):
        continue
    df = pd.read_csv(lfp)
    collect_data(ticker, batch_data_dict, df)

write_data(worker_idx, batch_data_dict)
