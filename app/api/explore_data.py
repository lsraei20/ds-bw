import pandas as pd
import numpy as np

df = pd.read_csv('/Users/israel/Desktop/kickstarter_data_with_features.csv')

# These are the only columns we can use as input
df = df[['name', 'goal', 'blurb', 'launched_at', 'deadline', 'category', 'state', 'country']]

# filter out all countries not english-speaking
english_countries = ['US', 'IE', 'GB', 'AU', 'CA', 'NZ', ]
df = df[df['country'].isin(english_countries)]

# create 'success'filter which only shows failed or success and cuts out other options
suc_filt = ['failed', 'successful']
df = df[df['state'].isin(suc_filt)]
# Convert fail or succuess to 0 or 1
df['state'] = df['state'].replace({'failed': 0, 'successful': 1})

# Two seperate dataframes are created below, one of only success and one of only fail
faileddf = df[df['state'] == 0]
sucdf = df[df['state'] == 1]

print(sucdf)
