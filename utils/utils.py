import numpy as np
import datetime


def i_to_date(i_date):
    return datetime.date(i_date // 10000, (i_date % 10000) // 100, i_date % 100)


def ema(prev_ema, val, gamma):
    return val * (1 - gamma) + gamma * prev_ema;


def arr_ema(arr, gamma):
    def _ema(prev_ema, val):
        return ema(prev_ema, val, gamma)

    v_ema = np.frompyfunc(_ema, 2, 1)

    return v_ema.accumulate(arr, dtype=np.object).astype(np.float)


def arr_rema(arr, gamma):
    intermediate = arr_ema(arr[::-1], gamma)
    return intermediate[::-1]


def _roll_fwd(prev, val):
    return prev if val <= 0 else val


_v_roll_fwd = np.frompyfunc(_roll_fwd, 2, 1)


def roll_arr_fwd(arr):
    return _v_roll_fwd.accumulate(arr, dtype=np.object).astype(np.float)


def roll_arr_bwd(arr):
    intermediate = roll_arr_fwd(arr[::-1])
    return intermediate[::-1]
