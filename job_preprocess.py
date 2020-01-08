import abstractions.job_queue as job_queue
import job_scheduler as jobs
from abstractions.log import log
import abstractions.file_storage as file_storage
import abstractions.constants as constants
import os
import numpy as np
import datetime
from utils.utils import arr_rema, i_to_date, date_to_i, roll_arr_fwd
import math
import tempfile
from abstractions.tiingo import get_tickers, START_DATE_COLUMN, END_DATE_COLUMN

# https://www.youtube.com/watch?v=ffDLG7Vt6JE&t=18s

ANN_FACTOR = 252.75


def get_indexes(i_dates: np.ndarray, min_date: datetime.date):
    indexes = np.zeros_like(i_dates)
    idx = 0
    for i in i_dates:
        indexes[idx] = (i_to_date(i_dates[idx]) - min_date).days
        idx = idx + 1
    return indexes


def get_raw_data(total_points, indexes: np.ndarray, data: np.ndarray):
    # ['v', 't', 'a_o', 'a_h', 'a_l', 'a_c']
    raw = np.zeros((total_points, 6))

    # ['date', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l', 'a_c', 'a_v', 'div', 'split']
    raw[indexes, 0] = data[:, 5]
    raw[indexes, 1] = (data[:, 2] + data[:, 3] + data[:, 4]) / 3
    raw[indexes, 2] = data[:, 6]
    raw[indexes, 3] = data[:, 7]
    raw[indexes, 4] = data[:, 8]
    raw[indexes, 5] = data[:, 9]

    # now we apply hacks
    zero_volume_mask = raw[:, 0] == 0
    # no trading activity interpreted as very small quantity
    raw[zero_volume_mask, 0] = 100

    # roll closing price
    raw[:, 5] = roll_arr_fwd(raw[:, 5])

    # copy closing price if other prices is missing
    zero_prices_mask = raw[:, 1] == 0
    raw[zero_prices_mask, 1] = raw[zero_prices_mask, 5]
    zero_prices_mask = raw[:, 2] == 0
    raw[zero_prices_mask, 2] = raw[zero_prices_mask, 5]
    zero_prices_mask = raw[:, 3] == 0
    raw[zero_prices_mask, 3] = raw[zero_prices_mask, 5]
    zero_prices_mask = raw[:, 4] == 0
    raw[zero_prices_mask, 4] = raw[zero_prices_mask, 5]

    return raw

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
    lr_rema_ann = ANN_FACTOR * lr_rema
    stddev_rema_ann = math.sqrt(ANN_FACTOR) * stddev_rema

    return np.stack([lr_rema_ann,
                     stddev_rema_ann], axis=1)


def save(ticker, spy_dates, spy_input, raw_input, raw_output, gamma):
    result = np.hstack([spy_dates, spy_input, raw_input, raw_output])
    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)

    # savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='',footer='', comments='# ', encoding=None):
    np.savetxt(tmp_file_name,
               result,
               fmt='%.0f %.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e %.18e',
               delimiter=',',
               comments='',
               header='date,spy_lr_o,spy_lr_h,spy_lr_l,spy_lr_c,spy_lr_gv,lr_o,lr_h,lr_l,lr_c,lr_gv,p_lr,p_std')
    file_storage.put_file(tmp_file_name, constants.DATA_BUCKET_NAME, f"preprocessed/{ticker}_{gamma}.csv")
    os.remove(tmp_file_name)


def preprocess(ticker, tmp_file_name, spy_tmp_file_name):
    eq_data = np.reshape(np.genfromtxt(tmp_file_name, delimiter=',', skip_header=1), (-1, 13))
    # do not process small datasets
    if eq_data.shape[0] <= 200:
        return
    spy_data = np.reshape(np.genfromtxt(spy_tmp_file_name, delimiter=',', skip_header=1), (-1, 13))
    # ['date', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l', 'a_c', 'a_v', 'div', 'split']

    spy_dates = spy_data[:, 0]
    # get dates
    i_spy_dates = spy_dates.astype(np.int)
    i_eq_dates = eq_data[:, 0].astype(np.int)

    # eq
    i_min_eq_date = i_eq_dates[0]
    i_max_eq_date = i_eq_dates[-1]
    min_eq_date = i_to_date(i_min_eq_date)
    max_eq_date = i_to_date(i_max_eq_date)
    # snp
    i_min_spy_date = i_spy_dates[0]
    i_max_spy_date = i_spy_dates[-1]
    min_spy_date = i_to_date(i_min_spy_date)
    max_spy_date = i_to_date(i_max_spy_date)

    # global indexes relatives to spy begin
    spy_indexes = get_indexes(i_spy_dates, min_spy_date)
    eq_indexes = get_indexes(i_eq_dates, min_spy_date)

    total_points = (max_spy_date - min_spy_date).days + 1
    spy_raw = get_raw_data(total_points, spy_indexes, spy_data)
    raw = get_raw_data(total_points, eq_indexes, eq_data)

    # now leave only active trading days: spy is traded
    spy_raw = spy_raw[spy_indexes, :]
    raw = raw[spy_indexes, :]

    spy_input = get_input_from_raw(spy_raw)

    # spy dates less than i_max_eq_date beacuse last day volume is usually 0 - price is fixed
    dates_mask = (spy_dates >= i_min_eq_date) & (spy_dates < i_max_eq_date)

    spy_input = spy_input[dates_mask, :]
    spy_dates = np.reshape(spy_dates, (-1, 1))
    spy_dates = spy_dates[dates_mask, :]

    raw = raw[dates_mask, :]
    raw_input = get_input_from_raw(raw)
    raw_output_95 = get_output(raw, 0.95)
    raw_output_90 = get_output(raw, 0.90)
    raw_output_80 = get_output(raw, 0.80)
    raw_output_70 = get_output(raw, 0.70)
    raw_output_50 = get_output(raw, 0.5)
    raw_output_00 = get_output(raw, 0.0)

    save(ticker, spy_dates, spy_input, raw_input, raw_output_95, 95)
    save(ticker, spy_dates, spy_input, raw_input, raw_output_90, 90)
    save(ticker, spy_dates, spy_input, raw_input, raw_output_80, 80)
    save(ticker, spy_dates, spy_input, raw_input, raw_output_70, 70)
    save(ticker, spy_dates, spy_input, raw_input, raw_output_50, 50)
    save(ticker, spy_dates, spy_input, raw_input, raw_output_00, 0)


spy_tmp_file_name = None

tickers = get_tickers()

while True:
    messages, to_ack = job_queue.pull_job_queue_items(jobs.PREPROCESS_QUEUE, 1)
    if len(messages) == 0:
        break
    for ticker in messages:
        ticker_info = tickers.query(f'ticker == "{ticker}"')
        if ticker_info.shape[0] == 0:
            continue
        sStartDate = ticker_info.iloc[0][START_DATE_COLUMN]
        sEndDate = ticker_info.iloc[0][END_DATE_COLUMN]
        if not isinstance(sStartDate, str) or not isinstance(sEndDate, str):
            continue
        start_date = datetime.datetime.strptime(sStartDate, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(sEndDate, "%Y-%m-%d")
        if (end_date - start_date).days <= 200:
            continue

        tmp_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, f"stocks/{ticker}.csv")
        if tmp_file_name is None:
            continue
        if spy_tmp_file_name is None:
            spy_tmp_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, "stocks/SPY.csv")
        log(f"Preprocessing {ticker} stock data")
        preprocess(ticker, tmp_file_name, spy_tmp_file_name)
        os.remove(tmp_file_name)

    job_queue.ack(jobs.PREPROCESS_QUEUE, to_ack)

if spy_tmp_file_name is not None:
    os.remove(spy_tmp_file_name)
