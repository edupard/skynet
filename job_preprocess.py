import abstractions.job_queue as job_queue
import job_scheduler as jobs
from abstractions.log import log
import abstractions.prices as prices
import abstractions.file_storage as file_storage
import abstractions.constants as constants
import os

def copy(ticker):
    tmp_file_name = file_storage.get_file(constants.DAILY_DATA_BUCKET_NAME, f"{ticker}.csv")
    if tmp_file_name is None:
        return
    file_storage.put_file(tmp_file_name, constants.DATA_BUCKET_NAME, f"stocks/{ticker}.csv")
    os.remove(tmp_file_name)


def preprocess (tmp_file_name, spy__tmp_file_name):
    i = 0

spy_tmp_file_name = None

while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.PREPROCESS_QUEUE, 1)
    if len(messages) == 0:
        break
    for ticker in messages:
        copy(ticker)
        # tmp_file_name = file_storage.get_file(constants.DAILY_DATA_BUCKET_NAME, f"{ticker}.csv")
        # if tmp_file_name is None:
        #     continue
        # if spy_tmp_file_name is None:
        #     spy_tmp_file_name = file_storage.get_file(constants.DAILY_DATA_BUCKET_NAME, f"spy.csv")
        # log(f"Preprocessing {ticker} stock data")
        # preprocess(tmp_file_name, spy_tmp_file_name)
        # os.remove(tmp_file_name)

    job_queue.ack(jobs.PREPROCESS_QUEUE, to_ack)

if spy_tmp_file_name is not None:
    os.remove(spy_tmp_file_name)