def get_worker_batch(worker_idx, num_workers, items):
    total = len(items)
    batch_size = (total // num_workers) + 1
    start = worker_idx * batch_size
    stop = start + batch_size
    to_process = items[start: stop]
    return to_process