import pandas as pd

def load_data(filepath):
    df = pd.read_csv(
        filepath,
        sep=' ',
        header=None,
        names=['date', 'time', 'sensor', 'state']
    )
    
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='mixed') # combine date + time to timestamp and convert to datetime object
    df = df.drop(columns=['date', 'time']) # delete date and time columns
    df['state'] = df['state'].map({'ON': 1, 'OFF': 0}) # convert ON/OFF to 1/0
    
    print(f"Loaded {len(df)} rows from {filepath}")
    print(df.head(5))
    return df

def compute_durations(df):
    # separate ON and OFF events
    on_events = df[df['state'] == 1].reset_index(drop=True)
    off_events = df[df['state'] == 0].reset_index(drop=True)
    
    # pair them together
    pairs = pd.DataFrame({
        'sensor': on_events['sensor'],
        'on_time': on_events['timestamp'],
        'off_time': off_events['timestamp'],
    })
    
    # compute duration in seconds
    pairs['duration_seconds'] = (pairs['off_time'] - pairs['on_time']).dt.total_seconds()
    
    print(f"Computed {len(pairs)} ON/OFF pairs")
    print(pairs.head())
    return pairs