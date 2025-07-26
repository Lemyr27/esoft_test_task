import logging
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

from src import config

logger = logging.getLogger(__name__)


def draw_graphs() -> None:
    old_data = pd.read_excel(config.get_excel_path())
    new_data = pd.read_csv('src/output/new_tdsk_apartments.csv')

    old_data['area'] = old_data['area'].apply(parse_area)

    _, axes = plt.subplots(1, 3, figsize=(12, 18))
    plt.subplots_adjust(hspace=0.4)

    width = 0.35

    logger.debug('Отображаются графики сравнения.')
    viewer = GraphViewer(axes, new_data, old_data, width)
    viewer.show_graphs()


def parse_area(value: datetime | float) -> float:
    if isinstance(value, datetime):
        return value.day + value.month / 100

    return float(value)


class GraphViewer:
    def __init__(self, axes, new_data: DataFrame, old_data: DataFrame, width: float):
        self.axes = axes
        self.new_data = new_data
        self.old_data = old_data
        self.width = width

    def draw_apartments_by_room_count(self) -> None:
        old_room_counts = self.old_data['room_count'].value_counts().sort_index()
        new_room_counts = self.new_data['room_count'].value_counts().sort_index()

        x = np.arange(len(old_room_counts))

        self.axes[0].bar(x - self.width / 2, old_room_counts, self.width, label='Старые данные')
        self.axes[0].bar(x + self.width / 2, new_room_counts, self.width, label='Новые данные')
        self.axes[0].set_xlabel('Количество комнат')
        self.axes[0].set_ylabel('Количество квартир')
        self.axes[0].set_title('Сравнение количества квартир по числу комнат')
        self.axes[0].legend()
        self.axes[0].set_xticks(x)
        self.axes[0].set_xticklabels(old_room_counts.index)

    def draw_apartments_by_area(self) -> None:
        bins_area = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]
        labels_area = ['<20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '>100']

        params = dict(bins=bins_area, labels=labels_area, right=False)
        old_areas = pd.cut(self.old_data['area'], **params).value_counts().sort_index()
        new_areas = pd.cut(self.new_data['area'], **params).value_counts().sort_index()

        x_area = np.arange(len(old_areas))

        self.axes[1].bar(x_area - self.width / 2, old_areas, self.width, label='Старые данные')
        self.axes[1].bar(x_area + self.width / 2, new_areas, self.width, label='Новые данные')
        self.axes[1].set_xlabel('Площадь (кв.м)')
        self.axes[1].set_ylabel('Количество квартир')
        self.axes[1].set_title('Сравнение количества квартир по площади')
        self.axes[1].set_xticks(x_area)
        self.axes[1].set_xticklabels(labels_area)
        self.axes[1].legend()

    def draw_apartments_by_price(self) -> None:
        bins_price = [0, 4e6, 5e6, 6e6, 7e6, 8e6, float('inf')]
        labels_price = ['<4млн', '4-5млн', '5-6млн', '6-7млн', '7-8млн', '>8млн']

        params = dict(bins=bins_price, labels=labels_price, right=False)
        old_prices = pd.cut(self.old_data['price'], **params).value_counts().sort_index()
        new_prices = pd.cut(self.new_data['price'], **params).value_counts().sort_index()

        x_price = np.arange(len(old_prices))

        self.axes[2].bar(x_price - self.width / 2, old_prices, self.width, label='Старые данные')
        self.axes[2].bar(x_price + self.width / 2, new_prices, self.width, label='Новые данные')
        self.axes[2].set_xlabel('Цена')
        self.axes[2].set_ylabel('Количество квартир')
        self.axes[2].set_title('Сравнение количества квартир по цене')
        self.axes[2].set_xticks(x_price)
        self.axes[2].set_xticklabels(labels_price)
        self.axes[2].legend()

    def show_graphs(self) -> None:
        self.draw_apartments_by_room_count()
        self.draw_apartments_by_area()
        self.draw_apartments_by_price()

        plt.tight_layout()
        plt.show()
