import pandas as pd
from pandas import DataFrame


def process_dates(df: DataFrame) -> None:
    df['published_at'] = pd.to_datetime(df['published_at'], format='ISO8601')
    df['actualized_at'] = pd.to_datetime(df['actualized_at'], format='ISO8601')
