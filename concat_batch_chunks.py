import utils.gcs as gcs
import numpy as np
import sys

worker_idx = int(sys.argv[1])
num_workers = int(sys.argv[2])

batch_id = worker_idx

gcs_client = gcs.GcsClient()

FROM = 1993
TO = 2021

chunks = []
for i in range(75):
    rfp = f'tiingo/batch_chunks/{FROM}_{TO}/{batch_id}_{i}.npy'
    lfp = f'/tmp/{batch_id}_{i}.npy'
    if not gcs_client.get(rfp, lfp):
        continue
    chunks.append(np.load(lfp))

batch = np.concatenate(chunks, axis=0)
lfp = f'/tmp/{batch_id}.npy'
rfp = f'tiingo/batches/{FROM}_{TO}/{batch_id}.npy'
np.save(lfp, batch)
gcs_client.save(lfp, rfp)
