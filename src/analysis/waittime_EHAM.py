""" Module that provides the estimated waittime for a given timestamp
    The timestamp is rounded to the nearest quarter hour """
import os.path
import pandas as pd
import numpy as np
import _pickle as pkl
from datetime import datetime

class WaitimeEHAS:
    def __init__(self, file):
        self._file = file
        self._dict = None
        self._pkl_file = "../../data/gulasch.pkl"
        if not os.path.isfile(self._pkl_file):
            df = self._load_data(self._file)
            self._dict = self._process_data(df)
            self._pickle(self._dict, self._pkl_file)
        else:
            self._dict = self._load_pickle(self._pkl_file)

    def _load_data(self, file):
        """ Loads data from a file """
        df = pd.read_csv(file, names=['DAY', 'INTERVAL', 'LANES_SECURITY', 'TRANSFERFILTER'], header=None, skiprows=1)
        return df

    def _process_data(self, df: pd.DataFrame):
        """ Brings the data in the correct format and aggregates information """
        # Create Datetime from DAY and INTERVAL_15MIN
        df['DATE'] = pd.to_datetime(df['DAY'] + ' ' + df['INTERVAL'], format='%Y-%m-%d %H:%M')
        # Calculate People per Security Lane
        df['PEOPLE_PER_LANE'] = df['TRANSFERFILTER'] / df['LANES_SECURITY']
        # Sort by Date ascending
        df = df.sort_values('DATE')

        # Add the Values for +15, +30 and +45 minutes and replace NaN with 0
        df['PEOPLE_PLUS_15'] = df.PEOPLE_PER_LANE.shift(-1)
        df['PEOPLE_PLUS_30'] = df.PEOPLE_PER_LANE.shift(-2)
        df['PEOPLE_PLUS_45'] = df.PEOPLE_PER_LANE.shift(-3)
        df.fillna(inplace=True, value=0)

    # Create Timestamp from DateTime
        df['TIMESTAMP'] = df.DATE.values.astype(np.int64) // 10 ** 9

    # Select Useful Information from DataFrame
        df_processed = df[['TIMESTAMP', 'PEOPLE_PER_LANE', 'PEOPLE_PLUS_15', 'PEOPLE_PLUS_30', 'PEOPLE_PLUS_45']]
        df_processed.set_index('TIMESTAMP', inplace=True)

        result = df_processed.T.to_dict()
        return result

    def _pickle(self, df, file):
        """ Pickles the waittime dictionary """
        with open(file, 'wb') as f:
            pkl.dump(df, f, -1)

    def get_predicted_waittime(self, ts):
        """ Gives the predicted waittimes for a given timestamp

            Keyword Arguments:

            ts -- epoch timestmap since 01.01.1970

            Returns Json:
            {'PEOPLE_PER_LANE': 7.333333333333333, 'PEOPLE_PLUS_15': 0.0,
            'PEOPLE_PLUS_30': 0.33333333333333331, 'PEOPLE_PLUS_45': 51.333333333333336} """
        dt = datetime.fromtimestamp(
            int(ts)
        )
        rounded_dt =  datetime(dt.year, dt.month, dt.day, dt.hour, 15*(dt.minute // 15))
        # rounded_ts = rounded_dt.astype(np.int64) // 10 ** 9
        rounded_ts = rounded_dt.timestamp()
        return self._dict[rounded_ts]


    def _load_pickle(self, pkl_file):
        """ Loads the dictionary from file"""
        return pkl.load(open(pkl_file, "rb"))

if __name__ == "__main__":
    eh = "../../data/EF.csv"
    gh = "../../data/GH.csv"
    object = WaitimeEHAS(eh)
#     eh_dict = process_data(load_data(eh))
#     gh_dict = process_data(load_data(gh))
    from pprint import pprint
    pprint(object.get_predicted_waittime("1497692825"))
