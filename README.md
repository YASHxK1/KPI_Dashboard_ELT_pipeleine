# KPI Dashboard ELT Pipeline

A Flask + SQLite KPI dashboard with a modular ELT pipeline.

## Current Maturity

This project started as a beginner-friendly prototype and now includes a cleaner module structure, basic validation, tests, and CI automation.

## Quick Start

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Run the app

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

## Environment Variables

- `DATA_PATH` (default: `Data/StoreSales.json`)
- `DB_PATH` (default: `sales_data.db`)
- `PORT` (default: `5000`)
- `FLASK_DEBUG` (default: `1`)

## Project Structure

```text
.
├── app.py                  # startup script
├── etl.py                  # extract/transform/load functions
├── metrics.py              # KPI calculation logic
├── web.py                  # Flask app factory and routes
├── templates/
│   └── dashboard.html      # dashboard template
├── tests/
│   ├── test_etl.py
│   ├── test_metrics.py
│   └── test_web.py
├── .github/workflows/ci.yml
├── requirements.txt
└── Data/StoreSales.json
```

## Features

- ELT from JSON source into SQLite.
- KPI calculations:
  - Total Sales
  - Total Profit
  - Total Quantity
  - Average Discount
  - Profit Margin (safe zero-division handling)
- Category and top-product summaries.
- `/healthz` route for lightweight health checks.

## Testing

```bash
pytest -q
```

## Notes

- Data validation checks required columns before loading.
- Numeric fields are coerced and cleaned in the transform step.
- CI runs tests on pushes and pull requests.
