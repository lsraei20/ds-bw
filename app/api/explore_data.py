import pandas as pd
import numpy as np

df = pd.read_csv('app/api/data/kickstarter_data_with_features.csv')

# These are the only columns we can use as input
df = df[['name', 'goal', 'blurb', 'launched_at', 'deadline', 'category', 'state', 'country']]

# filter out all countries not english-speaking
english_countries = ['US', 'IE', 'GB', 'AU', 'CA', 'NZ', ]
df = df[df['country'].isin(english_countries)]

# create 'success' filter which only shows failed or success and cuts out other options
suc_filt = ['failed', 'successful']
df = df[df['state'].isin(suc_filt)]
# Convert fail or success to 0 or 1
df['state'] = df['state'].replace({'failed': 0, 'successful': 1})

# separate dataframe created below, one of only success
sucdf = df[df['state'] == 1]

# monetary goal
monetary_goal_avg = sucdf['goal'].median()
print(monetary_goal_avg)


# title length
def length(df):
    return len(df)


sucdf['name_len'] = sucdf['name'].apply(length)
title_length = sucdf['name_len'].mean()
print(title_length)

# description length
sucdf['blurb_len'] = sucdf['blurb'].apply(length)
blurb_length = sucdf['blurb_len'].median()
print(blurb_length)


# campaign length
def campaign_len(df):
    df['deadline'] = df['deadline'].str[:10]
    df['launched_at'] = df['launched_at'].str[:10]
    df['deadline'] = pd.to_datetime(df['deadline'], format="%Y/%m/%d")
    df['launched_at'] = pd.to_datetime(df['launched_at'], format="%Y/%m/%d")
    # create new column
    df['cam_length'] = df['deadline'] - df['launched_at']
    return df


campaign_len_days = campaign_len(df)['cam_length'].mean().days
print(campaign_len_days)

# Month feedback
sucdf["month_launched"] = sucdf['launched_at']
sucdf["month_launched"] = pd.to_datetime(sucdf["month_launched"], format="%Y/%m/%d")
df["month_launched"] = df['launched_at']
df["month_launched"] = pd.to_datetime(df["month_launched"], format="%Y/%m/%d")


def extract_month(df):
    return df.month


sucdf['month_launched'] = sucdf['month_launched'].apply(extract_month)
df['month_launched'] = df['month_launched'].apply(extract_month)


def separate(df):
    df = df.reset_index(drop=True)
    dic = {}
    for row in range(df['month_launched'].value_counts().sum()):
        if df.loc[row, 'month_launched'] in dic.keys():
            dic[df.loc[row, 'month_launched']] += 1
        else:
            dic[df.loc[row, 'month_launched']] = 1
    return dic


successful_dict = separate(sucdf)
total_dict = separate(df)
month_probability_dic = ({k: successful_dict[k] / total_dict[k] for k in total_dict.keys() & successful_dict})
print(month_probability_dic)


