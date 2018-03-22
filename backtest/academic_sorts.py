import utils.price as price_utils
import pandas as pd

def get_single_sorts(signal, date, bins):
    rets = price_utils.get_daily_returns()
    bins = pd.cut(signal, bins)


class SimpleSort(object):
    def __init__(self):
        self.ret_df = price_utils.get_useful_price_df().set_index(['ticker', 'date']).loc[:, ['adj_close', 'adj_open']]

    def load_signal(self, signal_ser, days_ahead=30):
        self.ret_df['signal'] = signal_ser.reindex(self.ret_df.index)
        signal_ser_index = self.ret_df['signal'].dropna().index
        signal_ser_enum = pd.Series(range(len(signal_ser_index)), index=signal_ser_index).reindex(self.ret_df.index)
        self.ret_df['signal_id'] = signal_ser_enum.fillna(how='ffill')

        fwd_open = self.ret_df.groupby('signal_id')['adj_open'].head(days_ahead)
        fwd_close = self.ret_df.groupby('signal_id')['adj_close'].head(days_ahead)



