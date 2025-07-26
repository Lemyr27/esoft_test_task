import logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()]
)

START_DATE = '2023-07-01'
END_DATE = '2023-12-31'

MAX_REQUEST_RETRIES = 5


def get_excel_path() -> Path:
    return Path('src/data/') / 'Экспозиция ТДСК с 01.07.2023 по 31.12.2023.xlsx'
