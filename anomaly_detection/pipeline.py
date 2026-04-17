import pandas as pd

def load_data(filepath):
    df = pd.read_csv(
        filepath,
        sep=' ',
        header=None,
        names=['date', 'time', 'sensor', 'state']
    )

    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='mixed')
    df = df.drop(columns=['date', 'time'])

    # keep raw state too (useful later)
    df['state'] = df['state'].map({'ON': 1, 'OFF': 0})

    print(f"Loaded {len(df)} rows from {filepath}")
    return df


def compute_sessions(df):
    sessions = []

    df = df.sort_values('timestamp').reset_index(drop=True)

    if len(df) == 0:
        return pd.DataFrame(columns=[
            "sensor", "start", "end", "duration_seconds"
        ])

    rows = df.itertuples(index=False)

    first = next(rows)
    session_start = first.timestamp
    current_sensor = first.sensor

    for row in rows:
        if row.sensor != current_sensor:
            sessions.append({
                "sensor": current_sensor,
                "start": session_start,
                "end": row.timestamp,
                "duration_seconds": (row.timestamp - session_start).total_seconds()
            })

            current_sensor = row.sensor
            session_start = row.timestamp

    return pd.DataFrame(sessions)