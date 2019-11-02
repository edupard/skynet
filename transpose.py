import tempfile
import os
from google.cloud import storage
from google.cloud import datastore
import numpy as np
from messages_pb2 import Chunk
import uuid
import datetime

db = datastore.Client('skynet-1984')


def publish_chunks(tickers):
    chunks = {}

    ticker_num = 1
    for ticker in tickers:
        print("%d - %s" % (ticker_num, ticker))
        ticker_num += 1
        # get csv file
        client = storage.Client()
        bucket = client.get_bucket('skynet-1984-data')
        save_bucket = client.get_bucket('skynet-1984-chunks')
        blob = bucket.get_blob(f'{ticker}.csv')
        if blob is None:
            continue

        fd, tmp_file_name = tempfile.mkstemp()
        os.close(fd)
        blob.download_to_filename(tmp_file_name)

        # read file
        data = np.genfromtxt(tmp_file_name, delimiter=',', skip_header=1)

        os.remove(tmp_file_name)

        if len(data.shape) == 1:
            continue

        for idx in range(data.shape[0]):
            values = data[idx, :]
            # ['date', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l', 'a_c', 'a_v', 'div', 'split'])
            date = int(values[0])
            y = date // 10000
            m = (date % 10000) // 100
            d = (date % 10000) % 100

            key = (y, m)
            if key in chunks:
                chunk = chunks[key]
            else:
                chunk = Chunk(year=y, month=m, dailyChunks={})
                chunks[key] = chunk

            o = values[1]
            h = values[2]
            l = values[3]
            c = values[4]
            v = values[5]
            a_o = values[6]
            a_h = values[7]
            a_l = values[8]
            a_c = values[9]
            a_v = values[10]
            div = values[11]
            split = values[12]

            daily_data = chunk.dailyChunks[d]

            sd = daily_data.data[ticker]
            sd.o = o
            sd.h = h
            sd.l = l
            sd.c = c
            sd.v = v
            sd.a_o = a_o
            sd.a_h = a_h
            sd.a_l = a_l
            sd.a_c = a_c
            sd.a_v = a_v
            sd.div = div
            sd.split = split

    for y in range(1980, datetime.datetime.today().year):
        for m in range(1, 13):
            key = (y, m)
            if key in chunks.keys():
                chunk = chunks[key]
                entity = datastore.Entity(key=db.key('chunks'))
                path = str(uuid.uuid1())
                entity['year'] = y
                entity['month'] = m
                entity['path'] = path
                db.put(entity)
                blob = save_bucket.blob(path)
                blob.upload_from_string(chunk.SerializeToString())