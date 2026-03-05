# KPI Dashboard ELT Pipeline

> A modular KPI Dashboard with an ELT (Extract, Load, Transform) pipeline using SQLite for storage and Flask for the web interface, featuring interactive charts, filters, and a modern dark-themed UI.

## 📊 Overview

This project demonstrates a production-ready data pipeline that extracts sales data from JSON, loads it into a SQLite database, transforms it to calculate key performance indicators, and displays the results in a rich, interactive web dashboard.

**Key Stats:**
- 📦 **51,291** sales records processed
- 💰 **$12.6M** in total sales
- 📈 **$1.47M** in total profit
- 🎯 **11.61%** profit margin

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+

### Installation

1. **Clone and install dependencies:**
   ```bash
   git clone <repo-url>
   cd KPI_Dashboard_ELT_pipeleine
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the dashboard:**
   - Open your browser to: **http://127.0.0.1:5000**

4. **Run ETL only (no server):**
   ```bash
   python app.py --etl
   ```

### Docker

```bash
docker-compose up --build
```

Open **http://localhost:5000** in your browser.

---

## 📁 Project Structure

```
KPI_Dashboard_ELT_pipeleine/
├── app.py                  # Entry point – wires ETL → web server
├── config.py               # Centralised configuration (env vars)
├── etl.py                  # Extract & Load – JSON → validate → SQLite
├── metrics.py              # KPI queries, filters, caching
├── web.py                  # Flask routes & application factory
├── requirements.txt        # Pinned dependencies
├── Dockerfile              # Container image
├── docker-compose.yml      # One-command deployment
├── templates/
│   └── dashboard.html      # Jinja2 template with Chart.js
├── tests/
│   ├── __init__.py
│   └── test_dashboard.py   # pytest suite (unit + integration)
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions – lint + test
├── Data/
│   └── StoreSales.json     # Source dataset
├── EDA/
│   ├── EDA.py
│   └── EDA.ipynb
└── README.md
```

---

## 🎯 Features

### ELT Pipeline

#### **Extract**
- Reads data from `Data/StoreSales.json` using pandas
- Handles 51,291 rows of sales data

#### **Load**
- Validates schema: required columns, numeric casting, null handling
- Safe profit margin calculation (guards against divide-by-zero)
- Creates/replaces SQLite `sales` table automatically

#### **Transform**
- Calculates 5 key KPIs using parameterised SQL queries
- Aggregates data by category, product, and month
- Supports dynamic filtering by category, region, and date range
- Results are cached with configurable TTL

### Web Dashboard

- **5 KPI Cards** with animated entrance effects:
  - 💰 Total Sales · 📈 Total Profit · 📦 Quantity Sold · 🏷️ Avg Discount · 📊 Profit Margin

- **Interactive Charts (Chart.js):**
  - Monthly revenue trend (line chart)
  - Sales by category (doughnut chart)

- **Filter Bar:**
  - Filter by Category, Region, Date Range
  - One-click reset

- **Data Tables:**
  - Sales by Category
  - Top 10 Products by Sales

- **Modern Dark UI:**
  - Inter font, glassmorphism cards, gradient header
  - Responsive grid layout
  - Micro-animations and hover effects
  - "Last updated" timestamp

---

## 🛠️ Configuration

All settings are driven by environment variables with sensible defaults:

| Variable            | Default                | Description                     |
| ------------------- | ---------------------- | ------------------------------- |
| `DATA_PATH`         | `Data/StoreSales.json` | Path to source JSON             |
| `DB_PATH`           | `sales_data.db`        | SQLite database path            |
| `FLASK_HOST`        | `127.0.0.1`            | Server bind address             |
| `FLASK_PORT`        | `5000`                 | Server port                     |
| `FLASK_DEBUG`       | `1`                    | Debug mode (`0` for production) |
| `FLASK_ENV`         | `development`          | Flask environment               |
| `CACHE_TTL_SECONDS` | `300`                  | KPI cache lifetime              |

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

**Test coverage includes:**
- ✅ ETL validation (missing columns, numeric coercion, null handling)
- ✅ KPI calculations (totals, margin, safe division)
- ✅ Filter logic (category, region, date range)
- ✅ Flask route rendering (dashboard, health check, query-string filters)

---

## 🏗️ Architecture

```
JSON File ──▶ etl.py ──▶ SQLite DB ──▶ metrics.py ──▶ web.py ──▶ Dashboard
   │            │            │             │              │
 Extract    Validate &     Store       KPI Queries     Flask +
             Clean                   + Caching       Chart.js
```

**Module responsibilities:**
- **`config.py`** – Single source of truth for all settings
- **`etl.py`** – Extract, validate, and load data
- **`metrics.py`** – SQL queries, business logic, caching
- **`web.py`** – Flask routes and template rendering
- **`app.py`** – Thin entry point that orchestrates everything

---

## 📈 Next Steps (Optional Enhancements)

- 📄 Export KPIs to CSV or PDF reports
- 🔐 Add user authentication
- 🗄️ Migrate to PostgreSQL for larger datasets
- 📊 Add more Chart.js visualisations (bar, radar)
- 🔄 Scheduled ETL re-runs with APScheduler

---

## ✅ Verification

- ✅ 13 automated tests passing
- ✅ GitHub Actions CI pipeline configured
- ✅ Structured logging throughout
- ✅ Containerised with Docker
- ✅ Zero startup failures from malformed data
- ✅ Dashboard renders under 1 second on baseline dataset

---
