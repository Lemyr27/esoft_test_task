import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series, DatetimeIndex

from src import config

logger = logging.getLogger(__name__)


def gen_csv_active_objects_by_day(df: DataFrame) -> None:
    process_corpus(df)

    logger.debug('Генерируется csv с активными объектами по дням.')
    pivot = get_active_objects(df)
    pivot.to_csv(Path('src/output/') / 'active_objects_by_day.csv', index=False)


def process_corpus(df: DataFrame) -> None:
    df['address_corpus'] = df['address'].str.extract(r'([\w .,()-]*), подъезд')[0].str.strip()


def get_active_objects(df: DataFrame) -> Series | None:
    dates = get_date_range()
    result = [group_by_address_corpus(df, day) for day in dates]

    pivot = pd.concat(result)
    return pivot[['day', 'address_corpus', 'active_count']]


def get_date_range() -> DatetimeIndex:
    start_date = pd.to_datetime(config.START_DATE)
    end_date = pd.to_datetime(config.END_DATE)
    return pd.date_range(start=start_date, end=end_date, tz='utc')


def group_by_address_corpus(df: DataFrame, day: datetime) -> DataFrame:
    active_mask = (df['published_at'] <= day) & (df['actualized_at'] >= day)
    active_on_day = df.loc[active_mask]
    grouped = active_on_day.groupby('address_corpus').size().reset_index(name='active_count')
    grouped['day'] = day
    return grouped
