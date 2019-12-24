from abstractions.job_queue import push_job_queue_items
from tickers import get_tickers
from abstractions.prices import TICKER_COLUMN

DOWNLOAD_QUEUE = "download"

def schedule_download():
    df = get_tickers()
    push_job_queue_items(DOWNLOAD_QUEUE, df[TICKER_COLUMN].values)