import global_settings as gsettings
import os
import pandas as pd
import functools
from datetime import datetime as dt
import utils.cachify as cachify


MAIN_PATH = os.path.join(gsettings.DATA_PATH, 'price_data')

@cachify.SimpleMemoize
def get_price_data():
    full_df = pd.read_csv(os.path.join(MAIN_PATH, 'full_data.csv'))
    full_df['date'] = pd.to_datetime(full_df['date'])
    return full_df

@cachify.SimpleMemoize
def get_monthly_price_data(date=dt.today()):
    date = pd.to_datetime(date)
    file_path = os.path.join(MAIN_PATH, 'monthly_data', '{}.pkl'.format(date.strftime('%Y%m')))
    if os.path.exists(file_path):
        return pd.read_pickle(file_path)
    full_df = get_price_data()
    subset_df = full_df.loc[(full_df['date'].dt.month==date.month) & (full_df['date'].dt.year==date.year)]
    subset_df.to_pickle(file_path)
    return subset_df


def get_useful_price_df():
    # pre-condition is that full_df is sorted
    file_path = os.path.join(MAIN_PATH, 'useful_price_df.pkl')
    if os.path.exists(file_path):
        return pd.read_pickle(file_path)
    full_df = get_price_data()
    full_df = full_df.loc[:, ['ticker', 'date', 'adj_open', 'adj_close']]
    full_df['prev_adj_open'] = full_df.groupby('ticker')['adj_open'].shift(1)
    full_df['next_adj_open'] = full_df.groupby('ticker')['adj_open'].shift(-1)
    full_df['prev_adj_close'] = full_df.groupby('ticker')['adj_close'].shift(1)
    full_df['next_adj_close'] = full_df.groupby('ticker')['adj_close'].shift(-1)
    full_df.to_pickle(file_path)
    return full_df


def get_daily_returns(date, type):
    raise NotImplementedError



