import sqlite3
import pandas as pd


def _safe_profit_margin(total_profit: float, total_sales: float) -> float:
    if total_sales == 0:
        return 0.0
    return (total_profit / total_sales) * 100


def calculate_kpis(db_path: str) -> dict:
    """Calculate all KPIs and tabular summaries from the SQLite database."""
    with sqlite3.connect(db_path) as conn:
        summary = pd.read_sql_query(
            """
            SELECT
                COALESCE(SUM(Sales), 0) AS total_sales,
                COALESCE(SUM(Profit), 0) AS total_profit,
                COALESCE(SUM(Quantity), 0) AS total_quantity,
                COALESCE(AVG(Discount), 0) AS avg_discount
            FROM sales
            """,
            conn,
        )

        top_products = pd.read_sql_query(
            """
            SELECT [Product Name], SUM(Sales) AS total_sales, SUM(Profit) AS total_profit
            FROM sales
            GROUP BY [Product Name]
            ORDER BY total_sales DESC
            LIMIT 10
            """,
            conn,
        )

        sales_by_category = pd.read_sql_query(
            """
            SELECT Category, SUM(Sales) AS total_sales, SUM(Profit) AS total_profit
            FROM sales
            GROUP BY Category
            ORDER BY total_sales DESC
            """,
            conn,
        )

    total_sales_value = float(summary['total_sales'][0])
    total_profit_value = float(summary['total_profit'][0])
    total_quantity_value = int(summary['total_quantity'][0])
    avg_discount_value = float(summary['avg_discount'][0])

    return {
        'total_sales': round(total_sales_value, 2),
        'total_profit': round(total_profit_value, 2),
        'total_quantity': total_quantity_value,
        'avg_discount': round(avg_discount_value * 100, 2),
        'profit_margin': round(_safe_profit_margin(total_profit_value, total_sales_value), 2),
        'top_products': top_products,
        'sales_by_category': sales_by_category,
    }
