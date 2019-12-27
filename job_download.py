import abstractions.job_queue as job_queue
import scheduler as jobs
from abstractions.log import log
import abstractions.prices as prices
import abstractions.file_storage as file_storage
import abstractions.constants as constants

while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.DOWNLOAD_QUEUE, 10)
    if len(messages) == 0:
        break
    for ticker in messages:
        log(f"Downloading {ticker} stock data")
        tmp_file_name = prices.download_daily_data(ticker)
        if tmp_file_name is None:
            continue
        file_name = f"{ticker}.csv"
        file_storage.put_file(tmp_file_name, constants.DATA_BUCKET_NAME, file_name)
    job_queue.ack(jobs.DOWNLOAD_QUEUE, to_ack)