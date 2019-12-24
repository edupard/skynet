from abstraction.job_queue import pull_job_queue_items, ack
from abstraction.log import log

while True:
    messages, to_ack = pull_job_queue_items("download", 10)
    for m in messages:
        log(f"Downloading {m} stock data")
    ack(to_ack)