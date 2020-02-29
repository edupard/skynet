import pandas as pd
import utils.gcs as gcs
import numpy as np

gcs_client = gcs.GcsClient()

lfp = f'/tmp/stock_samples.csv'
rfp = f'tiingo/stock_samples.csv'

# get spy data
gcs_client.get(rfp, lfp)
df = pd.read_csv(lfp)

UP_TO_YEAR = 2021
UP_TO_DATE = UP_TO_YEAR * 10000 + 101

df = df.loc[df.date < UP_TO_DATE]

NUM_BATCHES = (UP_TO_YEAR - 1993) * 500 * 252 // 100000
df['batchId'] = np.random.randint(0, NUM_BATCHES, df.shape[0])
lfp = f"/tmp/samples_up_to_{UP_TO_YEAR}.csv"
rfp = f"tiingo/samples_up_to_{UP_TO_YEAR}.csv"
df.to_csv(lfp, index=False)

gcs_client.save(lfp, rfp)



