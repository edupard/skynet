from abstractions.samples_repo import SamplesRepo
from abstractions.batch_chunks_repo import BatchChunksRepo
import abstractions.constants as constants
import abstractions.file_storage as file_storage
import numpy as np
import os
import tempfile
import uuid
import sys
from abstractions.tiingo import TICKER_COLUMN, get_tickers
from abstractions.log import log
from tickers_util import get_tickers_chunk

TS = 100
DIM = 22

def write_data(worker_idx, repo: BatchChunksRepo, batch_data_dict):
    for batch_id, data in batch_data_dict.items():
        log(f"{worker_idx}: writing {batch_id} batch data")
        # create unique id
        sUuid = str(uuid.uuid1())

        # save chunk in repo
        repo.create(worker_idx, batch_id, sUuid)

        # get data to save
        idx, capacity, arr = data
        slice_to_save = arr[0:idx,:,:]

        # save np array
        np.save("tmp.npy", slice_to_save)

        # put to bucket
        file_storage.put_file("tmp.npy", constants.DATA_BUCKET_NAME, f"batch_chunks/{batch_id}_{sUuid}.csv")

        # cleanup - remove tmp file
        os.remove("tmp.npy")

def collect_data(ticker, batch_data_dict, data):
    dates_dict = {}
    idx = 0
    for date in data[:, 0]:
        iDate = int(date)
        dates_dict[iDate] = idx
        idx = idx + 1

    repo = SamplesRepo()
    samples = repo.get(ticker)

    for sample in samples:
        batch_id = sample['batch_id']
        date = sample['date']
        if date not in dates_dict:
            continue
        end_idx = dates_dict[date]
        if end_idx < (TS - 1):
            continue
        sample_data = data[end_idx - (TS - 1): end_idx + 1, 1:]

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

worker_idx, tickers = get_tickers_chunk(300)

# make job idempotent
log(f"{worker_idx}: cleanup")
repo = BatchChunksRepo()
chunks = repo.get_by_worker(worker_idx)
for chunk in chunks:
    batch_id = chunk['batch_id']
    sUuid = chunk['uuid']
    file_storage.remove_file(constants.DATA_BUCKET_NAME, f"batch_chunks/{batch_id}_{sUuid}.csv")
repo.remove_by_worker(worker_idx)

batch_data_dict = {}

ticker_idx = 0
for ticker in tickers:
    ticker_idx = ticker_idx + 1
    log(f"{worker_idx}: processing {ticker} #{ticker_idx}")
    tmp_file_name_00 = file_storage.get_file(constants.DATA_BUCKET_NAME, f"preprocessed/{ticker}_0.csv")
    if tmp_file_name_00 is None:
        continue
    tmp_file_name_50 = file_storage.get_file(constants.DATA_BUCKET_NAME, f"preprocessed/{ticker}_50.csv")
    if tmp_file_name_50 is None:
        continue
    tmp_file_name_70 = file_storage.get_file(constants.DATA_BUCKET_NAME, f"preprocessed/{ticker}_70.csv")
    if tmp_file_name_70 is None:
        continue
    tmp_file_name_80 = file_storage.get_file(constants.DATA_BUCKET_NAME, f"preprocessed/{ticker}_80.csv")
    if tmp_file_name_80 is None:
        continue
    tmp_file_name_90 = file_storage.get_file(constants.DATA_BUCKET_NAME, f"preprocessed/{ticker}_90.csv")
    if tmp_file_name_90 is None:
        continue
    tmp_file_name_95 = file_storage.get_file(constants.DATA_BUCKET_NAME, f"preprocessed/{ticker}_95.csv")
    if tmp_file_name_95 is None:
        continue

    # read file
    data_00 = np.reshape(np.genfromtxt(tmp_file_name_00, delimiter=' ', skip_header=1), (-1, 13))
    data_50 = np.reshape(np.genfromtxt(tmp_file_name_50, delimiter=' ', skip_header=1), (-1, 13))
    data_70 = np.reshape(np.genfromtxt(tmp_file_name_70, delimiter=' ', skip_header=1), (-1, 13))
    data_80 = np.reshape(np.genfromtxt(tmp_file_name_80, delimiter=' ', skip_header=1), (-1, 13))
    data_90 = np.reshape(np.genfromtxt(tmp_file_name_90, delimiter=' ', skip_header=1), (-1, 13))
    data_95 = np.reshape(np.genfromtxt(tmp_file_name_95, delimiter=' ', skip_header=1), (-1, 13))

    os.remove(tmp_file_name_00)
    os.remove(tmp_file_name_50)
    os.remove(tmp_file_name_70)
    os.remove(tmp_file_name_80)
    os.remove(tmp_file_name_90)
    os.remove(tmp_file_name_95)

    data_arr = [data_00, data_50[:, 11:], data_70[:, 11:], data_80[:, 11:], data_90[:, 11:], data_95[:, 11:]]
    data = np.hstack(data_arr)

    collect_data(ticker, batch_data_dict, data)

write_data(worker_idx, repo, batch_data_dict)
