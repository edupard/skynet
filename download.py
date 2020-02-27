import pandas as pd
from tiingo import TiingoClient
import os

import utils.messaging as messaging
from abstractions.log import log
import utils.gcs as gcs


# create tiingo client
def get_tiingo_client() -> TiingoClient:
    tiingo_config = {}
    tiingo_config['session'] = True
    tiingo_config['api_key'] = os.environ['TIINGO_API_KEY']
    return TiingoClient(tiingo_config)


tiingo_client = get_tiingo_client()


def download_daily_data(ticker):
    json = tiingo_client.get_ticker_price(ticker,
                                          fmt='json',
                                          startDate="1993-01-29",
                                          endDate="2020-02-26",
                                          frequency='daily')
    if len(json) == 0:
        return None
    df = pd.DataFrame(json)
    df = df.rename(columns={
        "date": "date",
        "open": "o",
        "high": "h",
        "low": "l",
        "close": "c",
        "volume": "v",
        "adjOpen": "a_o",
        "adjHigh": "a_h",
        "adjLow": "a_l",
        "adjClose": "a_c",
        "adjVolume": "a_v",
        "divCash": "div",
        "splitFactor": "split"
    })
    df = df[["date", "o", "h", "l", "c", "v", "a_o", "a_h", "a_l", "a_c", "a_v", "div", "split"]]
    df["date"] = df["date"].apply(lambda x: int(x[:10].replace("-", "")))
    return df


gcs_client = gcs.GcsClient()
subscriber = messaging.Subscriber()

while True:
    messages, to_ack = subscriber.pull_messages('tickers', 10)
    if len(messages) == 0:
        break
    for ticker in messages:
        log(f"Downloading {ticker} stock data")

        try:
            df = download_daily_data(ticker)
        except:
            print(f"Can't download {ticker} !!!")
            continue
        if df is None:
            continue
        lfp = f'/tmp/{ticker}.csv'
        rfp = f'tiingo/stocks/{ticker}.csv'
        df.to_csv(lfp, index=False)
        gcs_client.save(lfp, rfp)
    subscriber.ack('tickers', to_ack)
