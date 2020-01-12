import abstractions.constants as constants
from abstractions.samples_repo import SamplesRepo
import abstractions.file_storage as file_storage
import numpy as np
import abstractions.log as log
import os
import sys

SAMPLE_FROM_TOP = 500 + 2

tmp_samples_file = file_storage.get_file(constants.DATA_BUCKET_NAME, f"sample.csv")
sample_dates_data = np.genfromtxt(tmp_samples_file, delimiter=',', skip_header=1)
os.remove(tmp_samples_file)

tmp_sample_stocks_file = file_storage.get_file(constants.DATA_BUCKET_NAME, f"sample_stocks.csv")
sample_stocks = np.genfromtxt(tmp_sample_stocks_file, delimiter=',', dtype='U20', skip_header=1)
os.remove(tmp_sample_stocks_file)

batch_id = int(sys.argv[1])
num_samples = int(sys.argv[2])
repo = SamplesRepo()
# cleanup
repo.remove(batch_id)

dates = sample_dates_data[:,0].astype(np.int)
stocks_per_day = sample_dates_data[:,1]
total_days = dates.shape[0]
date_prob = stocks_per_day / np.sum(stocks_per_day)

dates_samples = np.random.choice(total_days, num_samples, p=date_prob)
tickers_samples = np.random.choice(SAMPLE_FROM_TOP, num_samples)

for i in range(num_samples):
    date_idx = dates_samples[i]
    ticker_idx = tickers_samples[i]
    i_date = int(dates[date_idx])
    ticker = sample_stocks[date_idx, ticker_idx]
    if ticker == "SPY" or ticker == "ZXZZT":
        continue
    repo.create(batch_id, ticker, i_date)
