"""
Test suite for the KPI Dashboard.

Covers:
  - ETL validation logic (unit)
  - Metric calculations (unit)
  - Flask route rendering (integration)
"""

import os
import sqlite3
import tempfile

import pandas as pd
import pytest

# ── Fixtures ────────────────────────────────────────────────────────────────

SAMPLE_DATA = [
    {
        "Row ID": 1,
        "Order ID": "ORD-001",
        "Order Date": "2023-01-15",
        "Ship Date": "2023-01-20",
        "Ship Mode": "Standard",
        "Customer ID": "CUS-001",
        "Customer Name": "Alice",
        "Segment": "Consumer",
        "City": "Seattle",
        "State": "Washington",
        "Country": "United States",
        "Postal Code": 98101,
        "Market": "US",
        "Region": "West",
        "Product ID": "PROD-001",
        "Category": "Technology",
        "Sub-Category": "Phones",
        "Product Name": "Widget A",
        "Sales": 1000.0,
        "Quantity": 5,
        "Discount": 0.1,
        "Profit": 200.0,
        "Shipping Cost": 25.0,
        "Order Priority": "High",
    },
    {
        "Row ID": 2,
        "Order ID": "ORD-002",
        "Order Date": "2023-02-10",
        "Ship Date": "2023-02-14",
        "Ship Mode": "Express",
        "Customer ID": "CUS-002",
        "Customer Name": "Bob",
        "Segment": "Corporate",
        "City": "Portland",
        "State": "Oregon",
        "Country": "United States",
        "Postal Code": 97201,
        "Market": "US",
        "Region": "West",
        "Product ID": "PROD-002",
        "Category": "Furniture",
        "Sub-Category": "Chairs",
        "Product Name": "Widget B",
        "Sales": 500.0,
        "Quantity": 2,
        "Discount": 0.2,
        "Profit": -50.0,
        "Shipping Cost": 15.0,
        "Order Priority": "Medium",
    },
    {
        "Row ID": 3,
        "Order ID": "ORD-003",
        "Order Date": "2023-03-05",
        "Ship Date": "2023-03-08",
        "Ship Mode": "Standard",
        "Customer ID": "CUS-003",
        "Customer Name": "Carol",
        "Segment": "Consumer",
        "City": "Denver",
        "State": "Colorado",
        "Country": "United States",
        "Postal Code": 80201,
        "Market": "US",
        "Region": "Central",
        "Product ID": "PROD-003",
        "Category": "Office Supplies",
        "Sub-Category": "Paper",
        "Product Name": "Widget C",
        "Sales": 0.0,
        "Quantity": 10,
        "Discount": 0.0,
        "Profit": 0.0,
        "Shipping Cost": 5.0,
        "Order Priority": "Low",
    },
]


@pytest.fixture()
def sample_df():
    """Return a small DataFrame mirroring the real schema."""
    return pd.DataFrame(SAMPLE_DATA)


@pytest.fixture()
def tmp_db(sample_df):
    """Create a temporary SQLite database pre-loaded with sample data."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    sample_df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()
    yield path
    os.unlink(path)


# ── ETL / Validation Tests ─────────────────────────────────────────────────

class TestValidation:
    def test_validate_success(self, sample_df):
        from etl import validate_dataframe
        result = validate_dataframe(sample_df.copy())
        assert len(result) == 3

    def test_validate_missing_column(self, sample_df):
        from etl import DataValidationError, validate_dataframe
        bad_df = sample_df.drop(columns=["Sales"])
        with pytest.raises(DataValidationError, match="Missing required columns"):
            validate_dataframe(bad_df)

    def test_validate_numeric_coercion(self, sample_df):
        from etl import validate_dataframe
        df = sample_df.copy()
        df.loc[0, "Sales"] = "not_a_number"
        result = validate_dataframe(df)
        assert result.loc[0, "Sales"] == 0.0

    def test_validate_null_category(self, sample_df):
        from etl import validate_dataframe
        df = sample_df.copy()
        df.loc[0, "Category"] = None
        result = validate_dataframe(df)
        assert result.loc[0, "Category"] == "Unknown"


# ── Metrics Tests ──────────────────────────────────────────────────────────

class TestMetrics:
    def test_kpi_totals(self, tmp_db):
        from metrics import calculate_kpis, invalidate_cache
        invalidate_cache()
        kpis = calculate_kpis(db_path=tmp_db)
        assert kpis["total_sales"] == 1500.0
        assert kpis["total_profit"] == 150.0
        assert kpis["total_quantity"] == 17

    def test_kpi_profit_margin(self, tmp_db):
        from metrics import calculate_kpis, invalidate_cache
        invalidate_cache()
        kpis = calculate_kpis(db_path=tmp_db)
        assert kpis["profit_margin"] == 10.0  # 150/1500*100

    def test_safe_margin_zero_sales(self):
        from metrics import _safe_margin
        assert _safe_margin(100, 0) == 0.0

    def test_filter_by_category(self, tmp_db):
        from metrics import calculate_kpis, invalidate_cache
        invalidate_cache()
        kpis = calculate_kpis(db_path=tmp_db, category="Technology")
        assert kpis["total_sales"] == 1000.0

    def test_filter_by_region(self, tmp_db):
        from metrics import calculate_kpis, invalidate_cache
        invalidate_cache()
        kpis = calculate_kpis(db_path=tmp_db, region="Central")
        assert kpis["total_sales"] == 0.0  # Widget C has 0 sales

    def test_filter_options(self, tmp_db):
        from metrics import get_filter_options
        opts = get_filter_options(db_path=tmp_db)
        assert "Technology" in opts["categories"]
        assert "West" in opts["regions"]


# ── Web / Integration Tests ────────────────────────────────────────────────

class TestWeb:
    def test_dashboard_renders(self, tmp_db, monkeypatch):
        monkeypatch.setattr("metrics.DB_PATH", tmp_db)
        from metrics import invalidate_cache
        invalidate_cache()
        from web import create_app
        app = create_app()
        client = app.test_client()
        resp = client.get("/")
        assert resp.status_code == 200
        html = resp.data.decode()
        assert "Sales KPI Dashboard" in html
        assert "$1,500.00" in html  # total sales for sample data

    def test_health_endpoint(self, tmp_db, monkeypatch):
        monkeypatch.setattr("metrics.DB_PATH", tmp_db)
        from web import create_app
        app = create_app()
        client = app.test_client()
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "ok"

    def test_filter_querystring(self, tmp_db, monkeypatch):
        monkeypatch.setattr("metrics.DB_PATH", tmp_db)
        from metrics import invalidate_cache
        invalidate_cache()
        from web import create_app
        app = create_app()
        client = app.test_client()
        resp = client.get("/?category=Technology")
        assert resp.status_code == 200
        html = resp.data.decode()
        assert "$1,000.00" in html
