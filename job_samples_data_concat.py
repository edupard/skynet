from abstractions.batch_chunks_repo import BatchChunksRepo
import abstractions.constants as constants
import abstractions.file_storage as file_storage
import numpy as np
import os
import job_scheduler as jobs
import abstractions.job_queue as job_queue

repo = BatchChunksRepo()

while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.CONCAT_SAMPLES_DATA_QUEUE, 1)
    if len(messages) == 0:
        break
    batch_id = int(messages[0])
    chunks = repo.get_by_batch(batch_id)
    sub_batches = []
    for chunk in chunks:
        batch_id = chunk['batch_id']
        sUuid = chunk['uuid']
        tmp_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, f"batch_chunks/{batch_id}_{sUuid}.csv")
        if tmp_file_name is None:
            continue
        sub_batches.append(np.load(tmp_file_name))
    if len(sub_batches) == 0:
        continue
    batch = np.vstack(sub_batches)
    # save bacth
    np.save("tmp.npy", batch)

    # put to bucket
    file_storage.put_file("tmp.npy", constants.DATA_BUCKET_NAME, f"batches/{batch_id}.npy")

    # cleanup - remove tmp file
    os.remove("tmp.npy")

    job_queue.ack(jobs.CONCAT_SAMPLES_DATA_QUEUE, to_ack)


