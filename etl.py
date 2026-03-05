import os
import sqlite3
import pandas as pd

REQUIRED_COLUMNS = {
    'Sales', 'Profit', 'Quantity', 'Discount', 'Category', 'Product Name'
}


def extract_data(data_path: str) -> pd.DataFrame:
    """Extract sales data from a JSON source file."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_json(data_path)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply basic data quality transformations before loading."""
    transformed = df.copy()

    numeric_columns = ['Sales', 'Profit', 'Quantity', 'Discount']
    for column in numeric_columns:
        transformed[column] = pd.to_numeric(transformed[column], errors='coerce')

    transformed[numeric_columns] = transformed[numeric_columns].fillna(0)
    transformed['Quantity'] = transformed['Quantity'].astype(int)

    return transformed


def load_to_database(df: pd.DataFrame, db_path: str, table_name: str = 'sales') -> int:
    """Load a dataframe into SQLite and return loaded row count."""
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    return len(df)


def run_elt(data_path: str, db_path: str) -> int:
    """Run extract-transform-load process and return number of rows loaded."""
    raw = extract_data(data_path)
    clean = transform_data(raw)
    return load_to_database(clean, db_path)
