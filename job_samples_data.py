import abstractions.constants as constants
import abstractions.file_storage as file_storage
import numpy as np
import abstractions.log as log
import tempfile
import os

from abstractions.constants import TOP_N, PRICE_LIMIT


def save_samples_data():
    spy_tmp_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, "stocks/SPY.csv")
    spy_data = np.reshape(np.genfromtxt(spy_tmp_file_name, delimiter=',', skip_header=1), (-1, 13))
    spy_dates = spy_data[:, 0]
    i_spy_dates = spy_dates.astype(np.int)

    dates = []
    totals = []
    tops = []

    for i_date in i_spy_dates:
        log.log(f"Processing {i_date}")

        dates.append(i_date)
        tmp_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, f"daily/{i_date}.csv")
        # ticker o h l c v a_o a_h a_l a_c a_v div split
        tickers = np.reshape(np.genfromtxt(tmp_file_name,
                                           dtype='U20',
                                           delimiter=',',
                                           usecols=0,
                                           skip_header=1,
                                           ), (-1, 1))
        total_tickers = tickers.shape[0]
        totals.append(total_tickers)

        daily_data = np.genfromtxt(tmp_file_name,
                                   delimiter=',',
                                   usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                   skip_header=1)
        os.remove(tmp_file_name)
        # filter out stocks with closing price less than 5
        price_mask = daily_data[:, 3] > PRICE_LIMIT
        daily_data = daily_data[price_mask, :]
        tickers = tickers[price_mask, :]
        # calc typical price
        h = daily_data[:, 1]
        l = daily_data[:, 2]
        c = daily_data[:, 3]
        v = daily_data[:, 4]
        t = (h + l + c) / 3
        gv = t * v
        sorted_indexes = np.argsort(-gv)
        sorted_tickers = tickers[sorted_indexes, :]
        top_tickers = sorted_tickers[0:TOP_N, :]

        tops.append(np.reshape(top_tickers, (1, TOP_N)))

    col_dates = np.reshape(np.array(dates), (-1, 1))
    col_totals = np.reshape(np.array(totals), (-1, 1))
    sample_dates = np.hstack([col_dates, col_totals])

    sample_stocks = np.vstack(tops)

    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    np.savetxt(tmp_file_name, sample_dates, fmt='%.0f', delimiter=',', comments='', header='date,traded')
    file_storage.put_file(tmp_file_name, constants.DATA_BUCKET_NAME, f"sample.csv")
    os.remove(tmp_file_name)

    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    np.savetxt(tmp_file_name, sample_stocks, fmt='%s', delimiter=',', comments='')
    file_storage.put_file(tmp_file_name, constants.DATA_BUCKET_NAME, f"sample_stocks.csv")
    os.remove(tmp_file_name)

save_samples_data()
