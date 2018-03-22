import pandas as pd
import os
import global_settings as gsettings


MAIN_PATH = os.path.join(gsettings.DATA_PATH, 'earnings_data')

def get_earnings_data():
    file_path = os.path.join(MAIN_PATH, 'earnings.csv')
    df = pd.read_csv(file_path)
    df = df.rename(columns={'symbol': 'ticker'})
    df['date'] = pd.to_datetime(df['date'])
    return df