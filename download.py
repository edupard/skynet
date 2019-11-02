from utils.tiingo import download_ticker_data_to_temp_file
from google.cloud import storage

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
        tmp_file_name = download_ticker_data_to_temp_file(ticker)
        file_name = f"{ticker}.csv"
        upload_file(tmp_file_name, file_name)
    except:
        print(f"{ticker} download failed")

def download_tickers(tickers):
    for ticker in tickers:
        process_ticker(ticker)