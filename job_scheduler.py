from abstractions.job_queue import push_job_queue_items
from abstractions.tickers import get_tickers
from abstractions.prices import TICKER_COLUMN

DOWNLOAD_QUEUE = "download"
TRANSPOSE_QUEUE = "transpose"
CONCAT_QUEUE = "concat"
PREPROCESS_QUEUE = "preprocess"

def schedule_download():
    df = get_tickers()
    push_job_queue_items(DOWNLOAD_QUEUE, df[TICKER_COLUMN].values)

def schedule_transpose():
    df = get_tickers()
    push_job_queue_items(TRANSPOSE_QUEUE, df[TICKER_COLUMN].values)

def schedule_preprocess():
    df = get_tickers()
    push_job_queue_items(PREPROCESS_QUEUE, df[TICKER_COLUMN].values)

def schedule_concat():
    dates = []
    for y in range(1993, 2020):
        for m in range(1,13):
            for d in range(1,32):
                date = y * 100 * 100 + m * 100 + d
                dates.append(str(date))
    push_job_queue_items(CONCAT_QUEUE, dates)