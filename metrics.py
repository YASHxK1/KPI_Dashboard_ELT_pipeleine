"""
Metrics / KPI module – Transform stage of the ELT pipeline.

All SQL queries and business logic for computing KPIs live here.
Results are returned as plain dicts / DataFrames so that the web
layer stays thin.
"""

import logging
import sqlite3
import time
from functools import lru_cache

import pandas as pd

from config import CACHE_TTL_SECONDS, DB_PATH

logger = logging.getLogger(__name__)


# ── Simple time-based cache ────────────────────────────────────────────────

_cache: dict = {}
_cache_ts: float = 0.0


def _is_cache_fresh() -> bool:
    return (time.time() - _cache_ts) < CACHE_TTL_SECONDS


def invalidate_cache() -> None:
    """Clear the KPI cache (useful after a fresh ETL run)."""
    global _cache, _cache_ts
    _cache = {}
    _cache_ts = 0.0
    logger.info("KPI cache invalidated.")


# ── Query helpers ───────────────────────────────────────────────────────────

def _get_connection(db_path: str | None = None) -> sqlite3.Connection:
    return sqlite3.connect(db_path or DB_PATH)


def _safe_margin(profit: float, sales: float) -> float:
    """Return profit margin %, guarding against divide-by-zero."""
    if sales == 0:
        return 0.0
    return round((profit / sales) * 100, 2)


# ── Public API ──────────────────────────────────────────────────────────────

def calculate_kpis(
    db_path: str | None = None,
    *,
    category: str | None = None,
    region: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:
    """Calculate all dashboard KPIs with optional filters.

    Parameters
    ----------
    db_path : str, optional
        Override the default DB path.
    category : str, optional
        Filter by product category.
    region : str, optional
        Filter by region.
    date_from : str, optional
        Start date (YYYY-MM-DD).
    date_to : str, optional
        End date (YYYY-MM-DD).

    Returns
    -------
    dict
        Keys: total_sales, total_profit, total_quantity, avg_discount,
              profit_margin, top_products (DataFrame),
              sales_by_category (DataFrame), last_updated (str).
    """
    # Build the cache key from filter params
    cache_key = (category, region, date_from, date_to)

    global _cache, _cache_ts
    if _is_cache_fresh() and cache_key in _cache:
        logger.debug("Returning cached KPIs for %s", cache_key)
        return _cache[cache_key]

    conn = _get_connection(db_path)
    try:
        where_clauses: list[str] = []
        params: list = []

        if category:
            where_clauses.append("Category = ?")
            params.append(category)
        if region:
            where_clauses.append("Region = ?")
            params.append(region)
        if date_from:
            where_clauses.append("[Order Date] >= ?")
            params.append(date_from)
        if date_to:
            where_clauses.append("[Order Date] <= ?")
            params.append(date_to)

        where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        # ── Scalar KPIs ─────────────────────────────────────────────────
        scalar_query = f"""
            SELECT
                COALESCE(SUM(Sales),    0) AS total_sales,
                COALESCE(SUM(Profit),   0) AS total_profit,
                COALESCE(SUM(Quantity), 0) AS total_quantity,
                COALESCE(AVG(Discount), 0) AS avg_discount
            FROM sales
            {where_sql}
        """
        row = pd.read_sql_query(scalar_query, conn, params=params).iloc[0]

        total_sales = float(row["total_sales"])
        total_profit = float(row["total_profit"])
        total_quantity = int(row["total_quantity"])
        avg_discount = round(float(row["avg_discount"]) * 100, 2)
        profit_margin = _safe_margin(total_profit, total_sales)

        # ── Top 10 products ─────────────────────────────────────────────
        top_products = pd.read_sql_query(
            f"""
            SELECT [Product Name],
                   SUM(Sales)  AS total_sales,
                   SUM(Profit) AS total_profit
            FROM sales
            {where_sql}
            GROUP BY [Product Name]
            ORDER BY total_sales DESC
            LIMIT 10
            """,
            conn,
            params=params,
        )

        # ── Sales by category ──────────────────────────────────────────
        sales_by_category = pd.read_sql_query(
            f"""
            SELECT Category,
                   SUM(Sales)  AS total_sales,
                   SUM(Profit) AS total_profit
            FROM sales
            {where_sql}
            GROUP BY Category
            ORDER BY total_sales DESC
            """,
            conn,
            params=params,
        )

        # ── Monthly trend ──────────────────────────────────────────────
        monthly_trend = pd.read_sql_query(
            f"""
            SELECT SUBSTR([Order Date], 1, 7) AS month,
                   SUM(Sales)  AS total_sales,
                   SUM(Profit) AS total_profit
            FROM sales
            {where_sql}
            GROUP BY month
            ORDER BY month
            """,
            conn,
            params=params,
        )

        kpis = {
            "total_sales": round(total_sales, 2),
            "total_profit": round(total_profit, 2),
            "total_quantity": total_quantity,
            "avg_discount": avg_discount,
            "profit_margin": profit_margin,
            "top_products": top_products,
            "sales_by_category": sales_by_category,
            "monthly_trend": monthly_trend,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Update cache
        _cache[cache_key] = kpis
        _cache_ts = time.time()

        logger.info("KPIs calculated (filters=%s)", cache_key)
        return kpis

    finally:
        conn.close()


def get_filter_options(db_path: str | None = None) -> dict:
    """Return distinct values for category, region, and date range.

    Returns
    -------
    dict
        Keys: categories (list[str]), regions (list[str]),
              min_date (str), max_date (str).
    """
    conn = _get_connection(db_path)
    try:
        categories = pd.read_sql_query(
            "SELECT DISTINCT Category FROM sales ORDER BY Category", conn
        )["Category"].tolist()

        regions = pd.read_sql_query(
            "SELECT DISTINCT Region FROM sales ORDER BY Region", conn
        )["Region"].tolist()

        date_range = pd.read_sql_query(
            "SELECT MIN([Order Date]) AS min_date, MAX([Order Date]) AS max_date FROM sales",
            conn,
        ).iloc[0]

        return {
            "categories": categories,
            "regions": regions,
            "min_date": date_range["min_date"],
            "max_date": date_range["max_date"],
        }
    finally:
        conn.close()
