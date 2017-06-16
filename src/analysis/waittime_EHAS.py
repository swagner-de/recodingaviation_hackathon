import pandas as pd
import numpy as np
import _pickle as pkl

def load_data(file):
    df = pd.read_csv(file, names = ['DAY', 'INTERVAL', 'LANES_SECURITY', 'TRANSFERFILTER'], header = None, skiprows = 1)
    return df

def process_data(df: pd.DataFrame):
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

def pickle(df, file):
    with open(file, 'wb') as f:
        pkl.dump(df, f, -1)

if __name__ == "__main__":
    eh = "../../data/EF.csv"
    gh = "../../data/GH.csv"
    eh_dict = process_data(load_data(eh))
    gh_dict = process_data(load_data(gh))
    pickle(eh_dict, "../../data/eh.pkl")
    pickle(gh_dict, "../../data/gh.pkl")
