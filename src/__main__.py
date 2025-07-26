import pandas as pd

from src import config, utils
from src.scripts.active_objects_by_day import gen_csv_active_objects_by_day
from src.scripts.apartments_graphs import draw_graphs
from src.scripts.graph_monthly_active_objects import display_graph_monthly_active_objects
from src.scripts.tdsk_parser import parse_tdsk_apartments


def main() -> None:
    df = pd.read_excel(config.get_excel_path())
    utils.process_dates(df)

    gen_csv_active_objects_by_day(df)
    display_graph_monthly_active_objects(df)
    parse_tdsk_apartments()
    draw_graphs()


if __name__ == '__main__':
    main()
