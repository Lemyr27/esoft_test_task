import logging

import matplotlib.pyplot as plt
from pandas import DataFrame

logger = logging.getLogger(__name__)


def display_graph_monthly_active_objects(df: DataFrame) -> None:
    date_to_month(df)

    logger.debug('Отображается график месячного количества активных объектов по комнатности.')
    monthly_room_counts = df.groupby(['month', 'room_count']).size().unstack(fill_value=0)
    generate_graph(monthly_room_counts)


def date_to_month(df: DataFrame) -> None:
    df['month'] = df['actualized_at'].dt.to_period('M')


def generate_graph(monthly_room_counts: DataFrame) -> None:
    monthly_room_counts.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title('Месячное количество активных объектов по комнатности')
    plt.xlabel('Месяц')
    plt.ylabel('Количество объектов')
    plt.legend(title='Комнатность')
    plt.show()
