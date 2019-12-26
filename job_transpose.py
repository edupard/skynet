import abstractions.job_queue as job_queue
import scheduler as jobs
import abstractions.constants as constants
import abstractions.file_storage as file_storage
import numpy as np
import os

while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.TRANSPOSE_QUEUE, 200)
    if len(messages) == 0:
        break
    for ticker in messages:
        tmp_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, f"{ticker}.csv")
        # read file
        data = np.genfromtxt(tmp_file_name, delimiter=',', skip_header=1)

        os.remove(tmp_file_name)

        if len(data.shape) == 1:
            continue



    job_queue.ack(jobs.DOWNLOAD_QUEUE, to_ack)