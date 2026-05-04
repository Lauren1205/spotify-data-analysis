import pandas as pd
import requests
import time

# 1. Load Data

def load_data(filename):
    if filename.endswith(".json"):
        df = pd.read_json(filename)
    elif filename.endswith(".csv"):
        df = pd.read_csv(filename)
    return df

def clean_data(df):

    # rename columns
    df = df.rename(columns={
    "endTime": "timestamp",
    "artistName": "artist",
    "trackName": "track",
    "msPlayed": "ms_played"
    })

    # convert time
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # create date columns
    df["date"] = df["timestamp"].dt.date
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day

    
    # standardize column names
    df.columns = df.columns.str.strip()

    # convert milliseconds to minutes
    df["minutes_played"] = df["ms_played"] / 60000

      # remove very short plays (not valuable data)
    if 'ms_played' in df.columns:
        df = df[df["ms_played"] > 30000] # under 30 seconds

    # remove non-music entries
    df = df[df["artist"] != "White Noise Radiance"]

    # remove duplicates 
    df = df.drop_duplicates(subset=["timestamp", "artist", "track"])

    # remove missing data
    df = df.dropna()
    
    return df

def clean_weather_data(weather):
    
    # convert time 
    weather["date"] = pd.to_datetime(weather["date"]).dt.date

    weather = weather[["date", "tavg", "prcp", "wspd"]]

    # rename columns
    weather = weather.rename(columns={
        "tavg": "avg_temp",
        "prcp": "total_precip",
        "wspd": "avg_windspeed"
    })

    weather = weather.dropna(subset=["date"])

    return weather
    

def join_weather(df, weather):
    df["date"] = pd.to_datetime(df["date"])
    weather["date"] = pd.to_datetime(weather["date"])

    df = df.merge(weather, on="date", how="left")
    
    return df

def top_artists(df):
    artists = df['artist'].value_counts().head(5)
    return artists
    

