from rmq import Consumer, HandlerInfo
from download import download_tickers
from transpose import publish_chunks
from preprocess import preprocess_tickers
from transpose_glue import collect_month_data

consumer = Consumer(
        {
            "download": HandlerInfo(100, download_tickers),
            "transpose": HandlerInfo(100, publish_chunks),
            "preprocess": HandlerInfo(1, preprocess_tickers)
         })
consumer.start()