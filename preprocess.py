import tempfile
import os
from google.cloud import storage
import numpy as np
import math
import traceback
import sys

ANN_FACTOR = 252.75


def ema(prev_ema, val, gamma):
    return val * (1 - gamma) + gamma * prev_ema


def arr_ema(arr, gamma):
    def _ema(prev_ema, val):
        return ema(prev_ema, val, gamma)

    v_ema = np.frompyfunc(_ema, 2, 1)

    return v_ema.accumulate(arr, dtype=np.object).astype(np.float)


def arr_rema(arr, gamma):
    intermediate = arr_ema(arr[::-1], gamma)
    return intermediate[::-1]


def process_ticker(ticker):
    # get csv file
    client = storage.Client()
    bucket = client.get_bucket('skynet-1984-data')
    blob = bucket.get_blob(f'{ticker}.csv')
    if blob is None:
        return

    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    blob.download_to_filename(tmp_file_name)

    # read file
    data = np.genfromtxt(tmp_file_name, delimiter=',', skip_header=1)

    # ['date', 'o', 'h', 'l', 'c', 'v', 'a_o', 'a_h', 'a_l', 'a_c', 'a_v', 'div', 'split']

    o = data[:, 1]
    h = data[:, 2]
    l = data[:, 3]
    c = data[:, 4]
    v = data[:, 5]

    t = (h + l + c) / 3
    gv = v * t

    gv_ema = arr_ema(gv, 0.95)

    a_o = data[:, 6]
    a_h = data[:, 7]
    a_l = data[:, 8]
    a_c = data[:, 9]
    a_v = data[:, 10]
    a_c_0 = a_c[0]
    a_c_t_min_1 = np.roll(a_c, 1, axis=0)
    a_c_t_min_1[0] = a_c_0

    lr_o = np.log(a_o / a_c_t_min_1)
    lr_h = np.log(a_h / a_c_t_min_1)
    lr_l = np.log(a_l / a_c_t_min_1)
    lr_c = np.log(a_c / a_c_t_min_1)
    v_pct = gv / gv_ema - 1

    sigma = lr_c * lr_c

    lr_c_t__plus_1 = np.roll(lr_c, -1, axis=0)
    lr_c_t__plus_1[-1] = 0
    sigma_t_plus_1 = np.roll(sigma, -1, axis=0)
    sigma_t_plus_1[-1] = 0

    lr_ema_70 = arr_rema(lr_c_t__plus_1, 0.70)
    sigma_ema_70 = arr_rema(sigma_t_plus_1, 0.70)
    stddev_ema_70 = np.sqrt(sigma_ema_70)
    lr_ema_70_ann = ANN_FACTOR * lr_ema_70
    stddev_ema_70_ann = math.sqrt(ANN_FACTOR) * stddev_ema_70

    lr_ema_82 = arr_rema(lr_c_t__plus_1, 0.82)
    sigma_ema_82 = arr_rema(sigma_t_plus_1, 0.82)
    stddev_ema_82 = np.sqrt(sigma_ema_82)
    lr_ema_82_ann = ANN_FACTOR * lr_ema_82
    stddev_ema_82_ann = math.sqrt(ANN_FACTOR) * stddev_ema_82

    lr_ema_91 = arr_rema(lr_c_t__plus_1, 0.91)
    sigma_ema_91 = arr_rema(sigma_t_plus_1, 0.91)
    stddev_ema_91 = np.sqrt(sigma_ema_91)
    lr_ema_91_ann = ANN_FACTOR * lr_ema_91
    stddev_ema_91_ann = math.sqrt(ANN_FACTOR) * stddev_ema_91

    lr_ema_95 = arr_rema(lr_c_t__plus_1, 0.95)
    sigma_ema_95 = arr_rema(sigma_t_plus_1, 0.95)
    stddev_ema_95 = np.sqrt(sigma_ema_95)
    lr_ema_95_ann = ANN_FACTOR * lr_ema_95
    stddev_ema_95_ann = math.sqrt(ANN_FACTOR) * stddev_ema_95

    result = np.concatenate([data,
                             np.reshape(lr_o, [-1, 1]),
                             np.reshape(lr_h, [-1, 1]),
                             np.reshape(lr_l, [-1, 1]),
                             np.reshape(lr_c, [-1, 1]),
                             np.reshape(v_pct, [-1, 1]),
                             np.reshape(lr_ema_70_ann, [-1, 1]),
                             np.reshape(stddev_ema_70_ann, [-1, 1]),
                             np.reshape(lr_ema_82_ann, [-1, 1]),
                             np.reshape(stddev_ema_82_ann, [-1, 1]),
                             np.reshape(lr_ema_91_ann, [-1, 1]),
                             np.reshape(stddev_ema_91_ann, [-1, 1]),
                             np.reshape(lr_ema_95_ann, [-1, 1]),
                             np.reshape(stddev_ema_95_ann, [-1, 1])
                             ], axis=1)
    np.savetxt(tmp_file_name,
               result,
               header='date,o,h,l,c,v,a_o,a_h,a_l,a_c,a_v,div,split,lr_o,lr_h,lr_l,lr_c,v_pct,lr_70,std_70,lr_82,std_82,lr_91,std_91,lr_95,std_95')

    bucket = client.get_bucket('skynet-1984-data-enriched')
    blob = bucket.blob(f'{ticker}.csv')
    blob.upload_from_filename(tmp_file_name)

    os.remove(tmp_file_name)


def preprocess_tickers(tickers):
    for ticker in tickers:
        try:
            process_ticker(ticker)
        except:
            traceback.print_exc(file=sys.stdout)
