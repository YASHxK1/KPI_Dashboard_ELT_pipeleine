"""
ETL module – Extract and Load stage of the ELT pipeline.

Responsibilities:
  1. Read the source JSON file.
  2. Validate the schema (required columns, data types).
  3. Clean / cast numeric columns and handle nulls.
  4. Load the validated DataFrame into a SQLite table.
"""

import logging
import sqlite3

import pandas as pd

from config import DATA_PATH, DB_PATH, REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


# ── Validation helpers ──────────────────────────────────────────────────────

class DataValidationError(Exception):
    """Raised when the source data fails validation checks."""


def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Verify required columns exist, cast numeric types, and fill nulls.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame read from the source file.

    Returns
    -------
    pd.DataFrame
        Cleaned and validated DataFrame.

    Raises
    ------
    DataValidationError
        If one or more required columns are missing.
    """
    # 1. Check required columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise DataValidationError(
            f"Missing required columns: {missing}"
        )

    # 2. Cast numeric columns (coerce invalid values → NaN → 0)
    numeric_cols = ["Sales", "Profit", "Quantity", "Discount", "Shipping Cost"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 3. Fill remaining NaN values in non-numeric columns
    df["Category"] = df["Category"].fillna("Unknown")
    df["Product Name"] = df["Product Name"].fillna("Unknown")
    df["Region"] = df["Region"].fillna("Unknown")

    # 4. Ensure Order Date is a proper datetime string
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    logger.info("Data validation passed – %d rows, %d columns", len(df), len(df.columns))
    return df


# ── Core ETL functions ──────────────────────────────────────────────────────

def extract(data_path: str | None = None) -> pd.DataFrame:
    """Read the JSON source file and return a raw DataFrame.

    Parameters
    ----------
    data_path : str, optional
        Override the default DATA_PATH from config.

    Returns
    -------
    pd.DataFrame
    """
    path = data_path or DATA_PATH
    logger.info("Extracting data from %s …", path)
    df = pd.read_json(path)
    logger.info("Extracted %d rows", len(df))
    return df


def load(df: pd.DataFrame, db_path: str | None = None) -> None:
    """Load a validated DataFrame into the SQLite ``sales`` table.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame to persist.
    db_path : str, optional
        Override the default DB_PATH from config.
    """
    path = db_path or DB_PATH
    logger.info("Loading %d rows into %s …", len(df), path)
    conn = sqlite3.connect(path)
    try:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        logger.info("Load complete.")
    finally:
        conn.close()


def run_etl(data_path: str | None = None, db_path: str | None = None) -> None:
    """Execute the full Extract → Validate → Load pipeline.

    Parameters
    ----------
    data_path : str, optional
        Override source JSON path.
    db_path : str, optional
        Override SQLite database path.
    """
    df = extract(data_path)
    df = validate_dataframe(df)
    load(df, db_path)
    logger.info("ETL pipeline finished successfully.")
