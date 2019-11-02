import tempfile
import os
from google.cloud import storage
from google.cloud import datastore
import numpy as np
from messages_pb2 import Chunk, DailyData
import uuid



def collect_month_data(months):
    month = 10
    year = 2018

    data = {}

    datastore_client = datastore.Client('skynet-1984')
    query = datastore_client.query(kind='chunks')

    storage_client = storage.Client()
    bucket = storage_client.get_bucket('skynet-1984-chunks')

    query.add_filter('month', '=', month)
    query.add_filter('year', '=', year)
    results = list(query.fetch())
    for r in results:
        # we need to collect at this level
        blob = bucket.get_blob(r['path'])
        bytes = blob.download_as_string()
        chunk = Chunk()
        chunk.ParseFromString(bytes)

        for day, daily_chunk in chunk.dailyChunks.iter():
            key = (year, month, day)
            if key in data:
                daily_data = data[key]
            else:
                daily_data = DailyData(day, {})
                data[key] = daily_data
            for ticker, ticker_data in daily_chunk.data.items():
                daily_data[ticker] = ticker_data
        for key, daily_data in data.items():
            year, month, day = key
            # we need to calc average volume, min, max, median, sort by volume
