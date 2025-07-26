import logging
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

from src import config

logger = logging.getLogger(__name__)


def parse_tdsk_apartments() -> None:
    base_url = "https://www.t-dsk.ru/buildings/search-apartments/"
    params = {"objects": "all"}
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
    }

    logger.debug('Запускается парсер ТДСК.')
    all_apartments = parse_all_apartments(base_url, headers, params)

    logger.debug('Данные собранные парсером генерируют csv.')
    df = pd.DataFrame(all_apartments)
    df.to_csv(Path('src/output/') / 'new_tdsk_apartments.csv', index=False)


def parse_all_apartments(base_url: str, headers: dict[str, str], params: dict[str, str]) -> list['Apartment']:
    all_apartments: list[Apartment] = []
    page = 1
    has_more = True

    retries = config.MAX_REQUEST_RETRIES

    while has_more:
        try:
            params['PAGEN_3'] = page

            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            current_apartments = parse_one_page_apartments(soup)
            all_apartments.extend(current_apartments)

            has_more = bool(soup.select_one('.search-result__more.load_more'))

            page += 1
            retries = config.MAX_REQUEST_RETRIES
        except Exception as e:
            retries -= 1
            if retries == 0:
                raise e

    return all_apartments


def parse_one_page_apartments(soup: BeautifulSoup) -> list['Apartment']:
    apartments: list[Apartment] = []
    for item in soup.select('.col-lg-3.col-md-4.col-sm-6.col-xs-12.flex-item'):
        try:
            processed_item = process_item(item)
            apartments.append(processed_item)
        except Exception as e:
            print(f"Ошибка парсинга элемента: {e}")
            continue

    return apartments


def process_item(item: Tag) -> 'Apartment':
    flat_link = item.select_one('.search-result__item-flat')

    flat_id = item.get('id', '').replace('bx_3218110189_', '')

    area_element = item.select_one('.search-result__item-area')
    area_match = re.search(r'(\d*,\d*)', area_element.text)
    area = float(area_match.group().replace(',', '.')) if area_match else "None"

    rooms = int(flat_link.get('data-rooms', "0")) if flat_link else 0

    floor_element = item.select_one('.search-result__item-floor')
    floor = int(floor_element.text) if floor_element else None

    flat_number = int(flat_link.get('data-number', '')) if flat_link else 0

    address_element = item.select_one('.search-result__address')
    address = address_element.text.strip() if address_element else ''

    gp_match = re.search(r'ГП-[^\s,)]+', address)
    gp = gp_match.group() if gp_match else ''

    entrance_number_match = re.search(r'(\d*) подъезд', address)
    entrance_number = int(entrance_number_match.group().split()[0]) if entrance_number_match else 'None'

    price_search = item.select_one('.search-result__price-base span').text.replace(' ', '')
    if not price_search.isdigit():
        price_search = item.select_one('.sale-price-season-search').next.strip().replace(' ', '')

    price = int(price_search)

    return Apartment(
        id=uuid.uuid4(),
        advert_id=flat_id,
        domain='t-dsk.ru',
        developer='ТДСК',
        address=address,
        gp=gp,
        description=address,
        entrance_number=entrance_number,
        floor=floor,
        area=area,
        room_count=rooms,
        flat_number=flat_number,
        price=price,
        published_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        actualized_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


class Apartment(TypedDict):
    id: uuid.UUID
    advert_id: str
    domain: str
    developer: str
    address: str
    gp: str
    description: str
    entrance_number: int
    floor: int
    area: float
    room_count: int
    flat_number: int
    price: int
    published_at: str
    actualized_at: str
