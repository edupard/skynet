from tiingo import TiingoClient
import csv
import tempfile
import os
import pandas as pd
import abstractions.constants as constants

TICKER_COLUMN = "ticker"

def _get_tiingo_client() -> TiingoClient:
    tiingo_config = {}
    tiingo_config['session'] = True
    tiingo_config['api_key'] = os.environ['TIINGO_API_KEY']
    return TiingoClient(tiingo_config)


def get_tickers():
    client = _get_tiingo_client()
    tickers = client.list_stock_tickers()
    matches = [el for el in tickers if
               (el['exchange'] == "NASDAQ" or el['exchange'] == "NYSE") and el['assetType'] == 'Stock']
    df = pd.DataFrame(matches, columns=matches[0].keys())
    df.rename(columns={"ticker": "ticker", "endDate": "endDate","startDate":"startDate","exchange":"exchange", "assetType":"assetType", "priceCurrency": "priceCurrency"})
    df = df.append({"ticker": "SPY", "endDate": "2019-12-23", "startDate": "1993-01-29", "exchange": "NYSE ARCA", "assetType": "Etf", "priceCurrency":"USD"}, ignore_index=True)
    return df


def _json_to_csv(ticker, json_data):
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

def _make_tiingo_request(client: TiingoClient, ticker):
    return client.get_ticker_price(ticker,
                                   fmt='json',
                                   startDate=constants.S_START_DATE,
                                   endDate=constants.S_END_DATE,
                                   frequency='daily')

def download_daily_data(ticker):
    client = _get_tiingo_client()
    json = _make_tiingo_request(client, ticker)
    if len(json) == 0:
        return None
    return _json_to_csv(ticker, json)