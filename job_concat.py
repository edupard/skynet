import abstractions.job_queue as job_queue
import job_scheduler as jobs
from abstractions.log import log
import abstractions.file_storage as file_storage
import abstractions.constants as constants
from abstractions.daily_chunks_repo import ChunksRepo
import os
import numpy as np
import tempfile
import csv

repo = ChunksRepo()


def write_data(date, dict):
    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    with open(tmp_file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['ticker', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l',
             'a_c', 'a_v', 'div', 'split'])
        for ticker, p in dict.items():
            o = p[0]
            h = p[1]
            l = p[2]
            c = p[3]
            v = p[4]
            a_o = p[5]
            a_h = p[6]
            a_l = p[7]
            a_c = p[8]
            a_v = p[9]
            div = p[10]
            split = p[11]
            writer.writerow([ticker, o, h, l, c, v, a_o, a_h, a_l, a_c, a_v, div, split])
    file_storage.put_file(tmp_file_name, constants.DATA_BUCKET_NAME, f"daily/{date}.csv")
    os.remove(tmp_file_name)


def read_data(chunk, dict):
    labels = np.reshape(np.genfromtxt(chunk, delimiter=',', skip_header=1, usecols=0, dtype=str), (-1, 1))
    data = np.reshape(np.genfromtxt(chunk, delimiter=',', skip_header=1), (-1,13))[:,1:]
    for idx in range(labels.shape[0]):
        values = data[idx, :]
        # ['date', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l', 'a_c', 'a_v', 'div', 'split'])
        ticker = labels[idx, 0]
        o = values[0]
        h = values[1]
        l = values[2]
        c = values[3]
        v = values[4]
        a_o = values[5]
        a_h = values[6]
        a_l = values[7]
        a_c = values[8]
        a_v = values[9]
        div = values[10]
        split = values[11]
        dict[ticker] = [o, h, l, c, v, a_o, a_h, a_l, a_c, a_v, div, split]


while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.CONCAT_QUEUE, 1)
    if len(messages) == 0:
        break
    for sDate in messages:
        log(f"Processing {sDate}")
        date = int(sDate)
        chunks = repo.get(date)
        dict = {}
        for chunk in chunks:
            tmp_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, f"tmp/{sDate}-{chunk['uuid']}.csv")
            if tmp_file_name is None:
                log(f"Can't find {chunk['uuid']}.csv")
                continue
            read_data(tmp_file_name, dict)
            os.remove(tmp_file_name)
        if not dict:
            continue
        write_data(date, dict)

    job_queue.ack(jobs.CONCAT_QUEUE, to_ack)
