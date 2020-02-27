import requests
import datetime
import pandas as pd
import numpy as np
import os
import utils.gcs as file_storage
import utils.constants as constants
import sys

spy_file_name = file_storage.get_file(constants.DATA_BUCKET_NAME, f"SPY.csv")
spy_data = np.reshape(np.genfromtxt(spy_file_name, delimiter=',', skip_header=1), (-1, 13))
spy_dates = spy_data[:, 0]
i_spy_dates = spy_dates.astype(np.int)

def i_to_date(i_date):
  return datetime.date(i_date // 10000, (i_date % 10000) // 100, i_date % 100)

POLYGON_API_KEY = os.environ['POLYGON_API_KEY']

params = {'apiKey': POLYGON_API_KEY, "unadjusted": True}
adj_params = {'apiKey': POLYGON_API_KEY, "unadjusted": False}

d = []
t = []
v = []
o = []
h = []
l = []
c = []

year = int(sys.argv[1])

for i_date in i_spy_dates:
  date = i_to_date(i_date)
  if date.year != year:
    continue

  s_date = date.strftime("%Y-%m-%d")
  print(s_date)
  while True:
    response = requests.get(f'https://api.polygon.io//v2/aggs/grouped/locale/us/market/stocks/{s_date}', params = params, timeout=60, stream=True)
    if response.status_code == 200:
      break
    else:
      print(response)
  json = response.json()
  if json['status'] == 'OK':
    for dp in json['results']:
      d.append(i_date)
      t.append(dp['T'])
      v.append(dp['v'])
      o.append(dp['o'])
      h.append(dp['h'])
      l.append(dp['l'])
      c.append(dp['c'])
  else:
    print(response)
    raise Exception(f'Failed to get data for {s_date}')

df = pd.DataFrame({'d': d, 't': t, 'v': v, 'o': o, 'h': h, 'l': l, 'c': c})
file_path = f"/tmp/{year}.csv"
df.to_csv(file_path, index=False)
file_storage.put_file(file_path, constants.DATA_BUCKET_NAME, f"polygon/daily/{year}.csv")