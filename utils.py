import pandas as pd

# 1. Load Data

def load_data(filename):
    df = pd.read_csv(filename, index_col=0)
    return df

def clean_data(df):
    # standardize column names
    df.columns = df.columns.str.strip()

    # convert time
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # remove missing data
    df = df.dropna()

    # remove very short plays (not valuable data)
    if 'ms_played' in df.columns:
        df = df[df["ms_played"] > 30000] # under 30 seconds
    
    return df

def top_artists(df):
    artists = df['artist'].value_counts().head(5)
    return artists
    

