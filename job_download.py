import abstractions.job_queue as job_queue
import scheduler as jobs
from abstractions.log import log
import abstractions.prices as prices
import abstractions.file_storage as file_storage

while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.DOWNLOAD_QUEUE, 10)
    if len(messages) == 0:
        break
    for ticker in messages:
        log(f"Downloading {ticker} stock data")
        tmp_file_name = prices.download_daily_data(ticker)

        file_name = f"{ticker}.csv"
        file_storage.put_file(tmp_file_name, file_name)
    job_queue.ack(jobs.DOWNLOAD_QUEUE, to_ack)