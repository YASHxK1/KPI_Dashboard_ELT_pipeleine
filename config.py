"""
Configuration module for KPI Dashboard.
Loads settings from environment variables with sensible defaults.
"""

import os

# ── Paths ───────────────────────────────────────────────────────────────────
DATA_PATH = os.environ.get("DATA_PATH", os.path.join("Data", "StoreSales.json"))
DB_PATH = os.environ.get("DB_PATH", "sales_data.db")

# ── Flask ───────────────────────────────────────────────────────────────────
FLASK_ENV = os.environ.get("FLASK_ENV", "development")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
FLASK_PORT = int(os.environ.get("FLASK_PORT", "5000"))
FLASK_HOST = os.environ.get("FLASK_HOST", "127.0.0.1")

# ── Cache ───────────────────────────────────────────────────────────────────
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "300"))  # 5 minutes

# ── Data Validation ────────────────────────────────────────────────────────
REQUIRED_COLUMNS = [
    "Sales",
    "Profit",
    "Quantity",
    "Discount",
    "Category",
    "Product Name",
    "Order Date",
    "Region",
    "Shipping Cost",
]
