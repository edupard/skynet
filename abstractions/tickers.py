from abstractions.file_storage import put_file, get_file
from abstractions.prices import get_tickers as get_tickers_impl
import abstractions.constants as constants
import os
import tempfile
import pandas as pd

def save_tickers():
    df = get_tickers_impl()
    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    df.to_csv(tmp_file_name, index=False)
    put_file(tmp_file_name, constants.DATA_BUCKET_NAME, "tickers.csv")

def get_tickers():
    local_file_name = get_file(constants.DATA_BUCKET_NAME, "tickers.csv")
    return pd.read_csv(local_file_name)