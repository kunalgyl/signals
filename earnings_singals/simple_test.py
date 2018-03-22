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

    bmo_ser, bmo_ret = get_signal_sers(bmo_ser, 'adj_open', 'adj_close')
    amc_ser, amc_ret = get_signal_sers(amc_ser, 'next_adj_open', 'next_adj_close')

    bmo_res = check_res(bmo_ser, bmo_ret, n_bins=n_bins)
    amc_res = check_res(amc_ser, amc_ret, n_bins=n_bins)
    combined_res = check_res(bmo_ser.combine_first(amc_ser), bmo_ret.combine_first(amc_ret), n_bins=n_bins)

    return bmo_res, amc_res, combined_res


def get_signal_sers(signal_ser, from_col, to_col):
    price_df = price_utils.get_useful_price_df().set_index(['ticker', 'date'])
    signal_ret = (price_df[to_col] / price_df[from_col]) - 1

    return signal_ser, signal_ret


def check_res(signal_ser, signal_ret, n_bins=10):
    signal_ser = pd.qcut(signal_ser, n_bins)

    price_df = price_utils.get_useful_price_df().set_index(['ticker', 'date'])
    price_df['signal_ser'] = signal_ser
    price_df['signal_ret'] = signal_ret

    signal_grp = price_df.groupby('signal_ser')['signal_ret']
    grp_mean = signal_grp.mean()
    grp_std = signal_grp.std()
    grp_count = signal_grp.count()
    grp_tsat = (grp_mean / grp_std) * grp_count.pow(1./2)

    return pd.DataFrame({'Mean': grp_mean, 'Std': grp_std, 'T-Stat': grp_tsat, 'Count': grp_count})