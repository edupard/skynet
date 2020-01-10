import abstractions.constants as constants
from abstractions.samples_repo import SamplesRepo
import abstractions.file_storage as file_storage
import numpy as np
import abstractions.log as log
import os
import sys

tmp_samples_file = file_storage.get_file(constants.DATA_BUCKET_NAME, f"sample.csv")
sample_dates = np.genfromtxt(tmp_samples_file, delimiter=',', skip_header=1)
os.remove(tmp_samples_file)

tmp_sample_stocks_file = file_storage.get_file(constants.DATA_BUCKET_NAME, f"sample_stocks.csv")
sample_stocks = np.genfromtxt(tmp_sample_stocks_file, delimiter=',', dtype='U20', skip_header=1)
os.remove(tmp_sample_stocks_file)

num_samples = int(sys.argv[1])
batch_id = int(sys.argv[1])
repo = SamplesRepo()

stocks_per_day = sample_stocks[:,1]
total_stocks = np.sum(stocks_per_day)
day_prob = stocks_per_day / total_stocks

days_samples = np.random.choice(5, num_samples, p=[0.1, 0, 0.3, 0.6, 0])
