import sqlite3
import pandas as pd
from metrics import calculate_kpis


def _seed_db(path: str, rows: list[dict]) -> None:
    df = pd.DataFrame(rows)
    with sqlite3.connect(path) as conn:
        df.to_sql('sales', conn, if_exists='replace', index=False)


def test_calculate_kpis_basic(tmp_path):
    db_path = tmp_path / 'sales.db'
    _seed_db(
        str(db_path),
        [
            {'Sales': 100, 'Profit': 10, 'Quantity': 2, 'Discount': 0.1, 'Category': 'Tech', 'Product Name': 'A'},
            {'Sales': 50, 'Profit': 5, 'Quantity': 1, 'Discount': 0.0, 'Category': 'Tech', 'Product Name': 'A'},
            {'Sales': 200, 'Profit': 20, 'Quantity': 4, 'Discount': 0.2, 'Category': 'Office', 'Product Name': 'B'},
        ],
    )

    kpis = calculate_kpis(str(db_path))

    assert kpis['total_sales'] == 350.0
    assert kpis['total_profit'] == 35.0
    assert kpis['total_quantity'] == 7
    assert kpis['avg_discount'] == 10.0
    assert kpis['profit_margin'] == 10.0
    assert len(kpis['top_products']) == 2
    assert len(kpis['sales_by_category']) == 2


def test_profit_margin_handles_zero_sales(tmp_path):
    db_path = tmp_path / 'sales_zero.db'
    _seed_db(
        str(db_path),
        [
            {'Sales': 0, 'Profit': 10, 'Quantity': 1, 'Discount': 0.1, 'Category': 'Tech', 'Product Name': 'A'},
        ],
    )

    kpis = calculate_kpis(str(db_path))
    assert kpis['profit_margin'] == 0.0
