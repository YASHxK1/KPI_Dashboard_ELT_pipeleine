# KPI Dashboard ELT Pipeline

> A KPI Dashboard with an ELT (Extract, Load, Transform) pipeline using SQLite for storage and Flask for the web interface.

## 📊 Overview

This project demonstrates a complete data pipeline that extracts sales data from JSON, loads it into a SQLite database, transforms it to calculate key performance indicators, and displays the results in a clean web dashboard.

**Key Stats:**
- 📦 **51,291** sales records processed
- 💰 **$12.6M** in total sales
- 📈 **$1.47M** in total profit
- 🎯 **11.61%** profit margin

---

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- Required packages: `pandas`, `flask`, `sqlite3`

### Installation

1. **Install dependencies:**
   ```bash
   pip install pandas flask
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the dashboard:**
   - Open your browser to: **http://127.0.0.1:5000**

4. **Stop the server:**
   - Press `CTRL+C` in the terminal

---

## 📁 Project Structure

```
Dashboard/
├── app.py # Main application (ELT pipeline + Flask)
├── sales_data.db # SQLite database 
├── README.md           
└── Data/
    └── StoreSales.json # Source dataset
```

---

## 🎯 Features

### ELT Pipeline

#### **Extract**
- Reads data from [Data/StoreSales.json](file:///e:/Local_projects/Dashboard/Data/StoreSales.json)
- Uses pandas `read_json()` for simple data loading
- Handles 51,291 rows of sales data

#### **Load**
- Creates SQLite database automatically
- Stores all data in a single `sales` table
- Uses pandas `to_sql()` for easy database insertion

#### **Transform**
- Calculates 5 key KPIs using SQL queries
- Aggregates data by category and product
- Computes profit margins and averages

### Web Dashboard

- **5 KPI Cards:**
  - 💰 Total Sales: $12,642,501.91
  - 📈 Total Profit: $1,467,457.29
  - 📦 Total Quantity Sold: 178,312 units
  - 🏷️ Average Discount: 14.29%
  - 📊 Profit Margin: 11.61%

- **Data Tables:**
  - Sales by Category (Technology, Furniture, Office Supplies)
  - Top 10 Products by Sales

- **Clean UI:**
  - Responsive design
  - Basic CSS styling
  - Easy-to-read layout

---

## 🛠️ Technical Details

### Code Structure

The [app.py] file contains:

1. **`load_data_to_database()`**
   - Extracts data from JSON
   - Loads into SQLite database
   - Prints confirmation message

2. **`calculate_kpis()`**
   - Runs SQL queries to calculate KPIs
   - Returns dictionary with all metrics
   - Includes aggregated data for tables

3. **Flask Routes**
   - Single route `/` displays the dashboard
   - Uses `render_template_string()` for simplicity
   - HTML template embedded in the same file

### Database Schema

Single table `sales` with 24 columns:
- **Order info:** Row ID, Order ID, Order Date, Ship Date, Ship Mode
- **Customer data:** Customer ID, Customer Name, Segment
- **Location:** City, State, Country, Postal Code, Market, Region
- **Product details:** Product ID, Category, Sub-Category, Product Name
- **Metrics:** Sales, Quantity, Discount, Profit, Shipping Cost, Order Priority

### KPI Calculations

- **Total Sales:** `SUM(Sales)`
- **Total Profit:** `SUM(Profit)`
- **Total Quantity:** `SUM(Quantity)`
- **Average Discount:** `AVG(Discount)`
- **Profit Margin:** `(Total Profit / Total Sales) × 100`

### Dependencies

- **pandas** - Data manipulation and JSON reading
- **sqlite3** - Database operations (built-in)
- **flask** - Web framework

---

## 🎓 Student-Friendly Design

This project is designed for beginners with:

✅ **Single file** - All code in one place  
✅ **No classes** - Uses simple functions only  
✅ **Clear comments** - Each section explained  
✅ **Basic SQL** - Simple SELECT and aggregate queries  
✅ **Inline HTML** - Template in same file for simplicity  
✅ **Print statements** - Shows progress in terminal  
✅ **No complex patterns** - Straightforward logic flow

---

## 📈 Next Steps (Optional Enhancements)

Want to extend this project? Consider:

- 📅 Add date filtering to view KPIs by time period
- 📊 Create charts using Chart.js or Plotly
- 🔍 Add more detailed product analysis
- 🌍 Implement regional performance comparison
- 📄 Export KPIs to CSV or PDF reports
- 🔐 Add user authentication
- 🎨 Enhance UI with modern CSS frameworks

---

## 📖 Documentation

For a detailed walkthrough of the implementation, see [walkthrough.md].

---

## ✅ Verification

The project has been tested and verified:
- ✅ Database created successfully (13.3 MB)
- ✅ All 51,291 rows loaded correctly
- ✅ KPIs calculated accurately
- ✅ Flask server runs without errors
- ✅ Dashboard displays properly in browser

---
