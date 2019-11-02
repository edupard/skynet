from tiingo import TiingoClient
import csv
import tempfile
import os
from google.cloud import storage

def json_to_csv(ticker, json_data):
    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    with open(tmp_file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['date', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l',
             'a_c', 'a_v', 'div', 'split'])
        for d in json_data:
            o = d['open']
            c = d['close']
            h = d['high']
            l = d['low']
            v = d['volume']
            adj_o = d['adjOpen']
            adj_c = d['adjClose']
            adj_h = d['adjHigh']
            adj_l = d['adjLow']
            adj_v = d['adjVolume']
            div_cash = d['divCash']
            split_factor = d['splitFactor']
            date = d['date'].split("T")[0].replace("-", "")
            writer.writerow(
                [date, o, h, l, c, v, adj_o, adj_h, adj_l, adj_c, adj_v, div_cash, split_factor])
    print(f"Data for {ticker} stored in {tmp_file_name}")
    return tmp_file_name

def get_tiingo_client() -> TiingoClient:
    config = {}
    config['session'] = True
    config['api_key'] = os.environ['TIINGO_API_KEY']
    return TiingoClient(config)

client = get_tiingo_client()

def make_tiingo_request(ticker):
    return client.get_ticker_price(ticker,
                                   fmt='json',
                                   startDate='1980-01-01',
                                   frequency='daily')

def upload_file(src_file_name, tgt_file_name):
    BUCKET_NAME = "skynet-1984-data"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(tgt_file_name)
    blob.upload_from_filename(src_file_name)

    print(f'File {src_file_name} uploaded to {BUCKET_NAME}/{tgt_file_name}.')

def process_ticker(ticker):
    print(f"processing {ticker}")
    try:
        json_data = make_tiingo_request(ticker)
        tmp_file_name = json_to_csv(ticker, json_data)
        file_name = f"{ticker}.csv"
        upload_file(tmp_file_name, file_name)
    except:
        print(f"{ticker} download failed")

def download_tickers(tickers):
    for ticker in tickers:
        process_ticker(ticker)