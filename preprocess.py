import utils.messaging as messaging
from abstractions.log import log
import numpy as np
import datetime
from utils.utils import arr_rema, i_to_date, roll_arr_fwd
import utils.gcs as gcs
import pandas as pd

gcs_client = gcs.GcsClient()


def get_idx_arr(i_dates: np.ndarray, min_date: datetime.date):
    indexes = np.zeros_like(i_dates)
    idx = 0
    for i in i_dates:
        indexes[idx] = (i_to_date(i_dates[idx]) - min_date).days
        idx = idx + 1
    return indexes


def get_raw_data(total_points, idx_arr, df):
    # ['v', 't', 'a_o', 'a_h', 'a_l', 'a_c']
    raw = np.zeros((total_points, 7))

    # ['date', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l', 'a_c', 'a_v', 'div', 'split']
    raw[idx_arr, 0] = df.v.values
    raw[idx_arr, 1] = (df.h.values + df.l.values + df.c.values) / 3
    raw[idx_arr, 2] = df.a_o.values
    raw[idx_arr, 3] = df.a_h.values
    raw[idx_arr, 4] = df.a_l.values
    raw[idx_arr, 5] = df.a_c.values
    raw[idx_arr, 6] = df.c.values

    # now we apply hacks
    zero_volume_mask = raw[:, 0] == 0
    # no trading activity interpreted as very small quantity
    raw[zero_volume_mask, 0] = 100

    # roll closing price
    raw[:, 5] = roll_arr_fwd(raw[:, 5])
    raw[:, 6] = roll_arr_fwd(raw[:, 6])

    # copy closing price if other prices is missing
    zero_prices_mask = raw[:, 1] == 0
    raw[zero_prices_mask, 1] = raw[zero_prices_mask, 6]
    zero_prices_mask = raw[:, 2] == 0
    raw[zero_prices_mask, 2] = raw[zero_prices_mask, 5]
    zero_prices_mask = raw[:, 3] == 0
    raw[zero_prices_mask, 3] = raw[zero_prices_mask, 5]
    zero_prices_mask = raw[:, 4] == 0
    raw[zero_prices_mask, 4] = raw[zero_prices_mask, 5]

    return raw[:,:6]


def get_input_from_raw(raw):
    gv = raw[:, 0] * raw[:, 1]
    a_o = raw[:, 2]
    a_h = raw[:, 3]
    a_l = raw[:, 4]
    a_c = raw[:, 5]

    a_c_0 = a_c[0]
    a_c_t_min_1 = np.roll(a_c, 1, axis=0)
    a_c_t_min_1[0] = a_c_0

    gv_0 = gv[0]
    gv_t_min_1 = np.roll(gv, 1, axis=0)
    gv_t_min_1[0] = gv_0

    lr_o = np.log(a_o / a_c_t_min_1)
    lr_h = np.log(a_h / a_c_t_min_1)
    lr_l = np.log(a_l / a_c_t_min_1)
    lr_c = np.log(a_c / a_c_t_min_1)
    lr_gv = np.log(gv / gv_t_min_1)

    result = np.stack([lr_o, lr_h, lr_l, lr_c, lr_gv], axis=1)
    return result


def get_output(raw, gamma):
    # gv, t, a_o, a_h, a_l, a_c
    a_c = raw[:, 5]
    a_c_0 = a_c[0]
    a_c_t_min_1 = np.roll(a_c, 1, axis=0)
    a_c_t_min_1[0] = a_c_0

    lr_c = np.log(a_c / a_c_t_min_1)
    sigma = lr_c * lr_c

    lr_c_t__plus_1 = np.roll(lr_c, -1, axis=0)
    lr_c_t__plus_1[-1] = 0
    sigma_t_plus_1 = np.roll(sigma, -1, axis=0)
    sigma_t_plus_1[-1] = 0

    lr_rema = arr_rema(lr_c_t__plus_1, gamma)
    sigma_rema = arr_rema(sigma_t_plus_1, gamma)
    stddev_rema = np.sqrt(sigma_rema)
    lr_rema_ann = lr_rema
    stddev_rema_ann = stddev_rema

    return np.stack([lr_rema_ann,
                     stddev_rema_ann], axis=1)


def preprocess(ticker, df, spy_df):
    # get dates
    i_spy_dates = spy_df.date.values.astype(np.int)
    i_dates = df.date.values.astype(np.int)

    # eq
    i_min_date = i_dates[0]
    i_max_date = i_dates[-1]
    min_date = i_to_date(i_min_date)
    max_date = i_to_date(i_max_date)
    # snp
    i_min_spy_date = i_spy_dates[0]
    i_max_spy_date = i_spy_dates[-1]
    min_spy_date = i_to_date(i_min_spy_date)
    max_spy_date = i_to_date(i_max_spy_date)

    # global indexes relatives to spy begin
    spy_idx_arr = get_idx_arr(i_spy_dates, min_spy_date)
    idx_arr = get_idx_arr(i_dates, min_spy_date)

    total_points = (max_spy_date - min_spy_date).days + 1
    spy_raw = get_raw_data(total_points, spy_idx_arr, spy_df)
    raw = get_raw_data(total_points, idx_arr, df)

    # now leave only active trading days: ie SPY is traded
    spy_raw = spy_raw[spy_idx_arr, :]
    raw = raw[spy_idx_arr, :]

    spy_input = get_input_from_raw(spy_raw)

    # spy dates less than i_max_date beacuse last day volume is usually 0 - price is fixed
    dates_mask = (i_spy_dates >= i_min_date) & (i_spy_dates < i_max_date)

    spy_input = spy_input[dates_mask, :]
    spy_dates = i_spy_dates[dates_mask]

    raw = raw[dates_mask, :]
    raw_input = get_input_from_raw(raw)
    raw_output = get_output(raw, 0.0)
    dict = {
        'date': spy_dates,
        'spy_lr_o': spy_input[:, 0],
        'spy_lr_h': spy_input[:, 1],
        'spy_lr_l': spy_input[:, 2],
        'spy_lr_c': spy_input[:, 3],
        'spy_lr_gv': spy_input[:, 4],
        'lr_o': raw_input[:, 0],
        'lr_h': raw_input[:, 1],
        'lr_l': raw_input[:, 2],
        'lr_c': raw_input[:, 3],
        'lr_gv': raw_input[:, 4],
        'p_lr': raw_output[:, 0]
    }
    df = pd.DataFrame(dict)
    lfp = f'/tmp/preprocessed_{ticker}.csv'
    rfp = f'tiingo/preprocessed/{ticker}.csv'
    df.to_csv(lfp, index=False)
    gcs_client.save(lfp, rfp)


gcs_client.get("tiingo/stocks/SPY.csv", '/tmp/SPY.csv')
gcs_client.get("tiingo/tickers.csv", '/tmp/tickers.csv')

spy_df = pd.read_csv('/tmp/SPY.csv')
tickers_df = pd.read_csv('/tmp/tickers.csv')

subscriber = messaging.Subscriber()

while True:
    messages, to_ack = subscriber.pull_messages('tickers', 1)
    if len(messages) == 0:
        break
    for ticker in messages:
        ticker_info = tickers_df.query(f'ticker == "{ticker}"')
        if ticker_info.shape[0] == 0:
            continue
        sStartDate = ticker_info.iloc[0].startDate
        sEndDate = ticker_info.iloc[0].endDate
        if not isinstance(sStartDate, str) or not isinstance(sEndDate, str):
            continue
        start_date = datetime.datetime.strptime(sStartDate, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(sEndDate, "%Y-%m-%d")
        if (end_date - start_date).days <= 65:
            continue

        rfp = f'tiingo/stocks/{ticker}.csv'
        lfp = f'/tmp/{ticker}.csv'
        gcs_client.get(rfp, lfp)
        df = pd.read_csv(lfp)

        log(f"Preprocessing {ticker} stock data")
        preprocess(ticker, df, spy_df)

    subscriber.ack('tickers', to_ack)
