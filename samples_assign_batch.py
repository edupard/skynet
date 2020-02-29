import pandas as pd
import utils.gcs as gcs
import numpy as np

gcs_client = gcs.GcsClient()

lfp = f'/tmp/stock_samples.csv'
rfp = f'tiingo/stock_samples.csv'

# get spy data
gcs_client.get(rfp, lfp)
df = pd.read_csv(lfp)

FROM = 1993
TO = 2021
FROM_DATE = 1993 * 10000 + 101
TO_DATE = TO * 10000 + 101

df = df.loc[(df.date < TO_DATE) & (df.date >= FROM_DATE)]

NUM_BATCHES = (TO - FROM) * 500 * 252 // 100000
df['batchId'] = np.random.randint(0, NUM_BATCHES, df.shape[0])
lfp = f"/tmp/samples_{FROM}_{TO}.csv"
rfp = f"tiingo/samples_{FROM}_{TO}.csv"
df.to_csv(lfp, index=False)

gcs_client.save(lfp, rfp)



