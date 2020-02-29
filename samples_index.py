import pandas as pd
import utils.gcs as gcs
import numpy as np

gcs_client = gcs.GcsClient()

# get spy data
gcs_client.get("tiingo/stocks/SPY.csv", '/tmp/SPY.csv')
spy_df = pd.read_csv('/tmp/SPY.csv')

i_spy_dates = spy_df.date.values.astype(np.int)
dfs = []
for i_date in i_spy_dates:
    print(i_date)
    rfp = f'tiingo/sample_stocks/{i_date}.csv'
    lfp = f'/tmp/{i_date}_samples.csv'
    if not gcs_client.get(rfp, lfp):
        continue
    df = pd.read_csv(lfp)
    df['date'] = i_date
    dfs.append(df)

df = pd.concat(dfs, axis=0)
lfp = f'/tmp/stock_samples.csv'
rfp = f'tiingo/stock_samples.csv'
df.to_csv(lfp, index=False)
gcs_client.save(lfp, rfp)


