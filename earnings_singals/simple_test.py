import utils.price as price_utils
import earnings_singals.read_data as ea_data
import backtest.academic_sorts as sorts
import pandas as pd


def get_ea_signal():
    earnings_df = ea_data.get_earnings_data()
    price_df = price_utils.get_useful_price_df()
    joined_df = earnings_df.merge(price_df, on=['ticker', 'date'], how='inner')

    bmo_df = joined_df.loc[joined_df['time'] == 'bmo'].set_index(['ticker', 'date'])
    amc_df = joined_df.loc[joined_df['time'] == 'amc'].set_index(['ticker' ,'date'])

    bmo_ser = (bmo_df['adj_open'] / bmo_df['prev_adj_close']).drop_duplicates()
    amc_ser = (amc_df['next_adj_open'] / amc_df['adj_close']).drop_duplicates()
    return bmo_ser, amc_ser


def get_sorts(n_bins=10):
    bmo_ser, amc_ser = get_ea_signal()

    bmo_res = get_signal_sorts(bmo_ser, 'adj_open', 'adj_close', n_bins=n_bins)
    amc_res = get_signal_sorts(amc_ser, 'next_adj_open', 'next_adj_close', n_bins=n_bins)

    return bmo_res, amc_res




def get_signal_sorts(signal_ser, from_col, to_col, n_bins=10):
    price_df = price_utils.get_useful_price_df().set_index(['ticker', 'date'])
    price_df['signal_ret'] = (price_df[to_col] / price_df[from_col]) - 1

    price_df['signal_ser'] = pd.qcut(signal_ser, n_bins)

    signal_grp = price_df.groupby('signal_ser')['signal_ret']
    grp_mean = signal_grp.mean()
    grp_std = signal_grp.std()
    grp_count = signal_grp.count()
    grp_tsat = (grp_mean / grp_std) * grp_count.pow(1./2)

    return pd.DataFrame({'Mean': grp_mean, 'Std': grp_std, 'T-Stat': grp_tsat, 'Count': grp_count})

