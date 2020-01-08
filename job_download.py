import abstractions.job_queue as job_queue
import job_scheduler as jobs
from abstractions.log import log
import abstractions.tiingo as tiingo
import abstractions.file_storage as file_storage
import abstractions.constants as constants

while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.DOWNLOAD_QUEUE, 10)
    if len(messages) == 0:
        break
    for ticker in messages:
        log(f"Downloading {ticker} stock data")
        try:
            tmp_file_name = tiingo.download_daily_data(ticker)
        except:
            continue
        if tmp_file_name is None:
            log(f"Failed to download {ticker} stock data")
            continue
        file_storage.put_file(tmp_file_name, constants.DATA_BUCKET_NAME, f"stocks/{ticker}.csv")
    job_queue.ack(jobs.DOWNLOAD_QUEUE, to_ack)