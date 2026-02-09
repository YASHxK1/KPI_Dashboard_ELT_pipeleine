# Simple KPI Dashboard - Beginner Student Code
# This is a basic ELT pipeline with Flask web interface

import sqlite3
import pandas as pd
from flask import Flask, render_template_string

# Step 1: Extract and Load data into SQLite
def load_data_to_database():
    """Load data from JSON file into SQLite database"""
    print("Loading data from JSON file...")
    
    # Read the JSON file
    df = pd.read_json('Data/StoreSales.json')
    
    # Connect to SQLite database (creates it if doesn't exist)
    conn = sqlite3.connect('sales_data.db')
    
    # Load data into a table called 'sales'
    df.to_sql('sales', conn, if_exists='replace', index=False)
    
    print(f"Loaded {len(df)} rows into database!")
    conn.close()

# Step 2: Calculate KPIs using SQL queries
def calculate_kpis():
    """Calculate all KPIs from the database"""
    conn = sqlite3.connect('sales_data.db')
    
    # Total Sales
    total_sales = pd.read_sql_query("SELECT SUM(Sales) as total FROM sales", conn)
    total_sales_value = total_sales['total'][0]
    
    # Total Profit
    total_profit = pd.read_sql_query("SELECT SUM(Profit) as total FROM sales", conn)
    total_profit_value = total_profit['total'][0]
    
    # Total Quantity Sold
    total_quantity = pd.read_sql_query("SELECT SUM(Quantity) as total FROM sales", conn)
    total_quantity_value = total_quantity['total'][0]
    
    # Average Discount
    avg_discount = pd.read_sql_query("SELECT AVG(Discount) as average FROM sales", conn)
    avg_discount_value = avg_discount['average'][0]
    
    # Profit Margin (Total Profit / Total Sales * 100)
    profit_margin = (total_profit_value / total_sales_value) * 100
    
    # Get top 10 products by sales
    top_products = pd.read_sql_query("""
        SELECT [Product Name], SUM(Sales) as total_sales, SUM(Profit) as total_profit
        FROM sales
        GROUP BY [Product Name]
        ORDER BY total_sales DESC
        LIMIT 10
    """, conn)
    
    # Get sales by category
    sales_by_category = pd.read_sql_query("""
        SELECT Category, SUM(Sales) as total_sales, SUM(Profit) as total_profit
        FROM sales
        GROUP BY Category
        ORDER BY total_sales DESC
    """, conn)
    
    conn.close()
    
    # Return all KPIs as a dictionary
    kpis = {
        'total_sales': round(total_sales_value, 2),
        'total_profit': round(total_profit_value, 2),
        'total_quantity': int(total_quantity_value),
        'avg_discount': round(avg_discount_value * 100, 2),  # Convert to percentage
        'profit_margin': round(profit_margin, 2),
        'top_products': top_products,
        'sales_by_category': sales_by_category
    }
    
    return kpis

# Step 3: Create Flask Web App
app = Flask(__name__)

# HTML template for the dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sales KPI Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .kpi-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        }
        .kpi-box {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 200px;
        }
        .kpi-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .section-title {
            font-size: 20px;
            margin-top: 30px;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>📊 Sales KPI Dashboard</h1>
    
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">${{ "{:,.2f}".format(kpis.total_sales) }}</div>
        </div>
        
        <div class="kpi-box">
            <div class="kpi-label">Total Profit</div>
            <div class="kpi-value">${{ "{:,.2f}".format(kpis.total_profit) }}</div>
        </div>
        
        <div class="kpi-box">
            <div class="kpi-label">Total Quantity Sold</div>
            <div class="kpi-value">{{ "{:,}".format(kpis.total_quantity) }}</div>
        </div>
        
        <div class="kpi-box">
            <div class="kpi-label">Average Discount</div>
            <div class="kpi-value">{{ kpis.avg_discount }}%</div>
        </div>
        
        <div class="kpi-box">
            <div class="kpi-label">Profit Margin</div>
            <div class="kpi-value">{{ kpis.profit_margin }}%</div>
        </div>
    </div>
    
    <h2 class="section-title">Sales by Category</h2>
    <table>
        <tr>
            <th>Category</th>
            <th>Total Sales</th>
            <th>Total Profit</th>
        </tr>
        {% for _, row in kpis.sales_by_category.iterrows() %}
        <tr>
            <td>{{ row['Category'] }}</td>
            <td>${{ "{:,.2f}".format(row['total_sales']) }}</td>
            <td>${{ "{:,.2f}".format(row['total_profit']) }}</td>
        </tr>
        {% endfor %}
    </table>
    
    <h2 class="section-title">Top 10 Products by Sales</h2>
    <table>
        <tr>
            <th>Product Name</th>
            <th>Total Sales</th>
            <th>Total Profit</th>
        </tr>
        {% for _, row in kpis.top_products.iterrows() %}
        <tr>
            <td>{{ row['Product Name'] }}</td>
            <td>${{ "{:,.2f}".format(row['total_sales']) }}</td>
            <td>${{ "{:,.2f}".format(row['total_profit']) }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page"""
    # Calculate KPIs
    kpis = calculate_kpis()
    
    # Render the HTML template with KPI data
    return render_template_string(HTML_TEMPLATE, kpis=kpis)

# Main execution
if __name__ == '__main__':
    print("=" * 50)
    print("Starting KPI Dashboard Setup...")
    print("=" * 50)
    
    # Step 1: Load data into database
    load_data_to_database()
    
    # Step 2: Calculate and display KPIs
    print("\nCalculating KPIs...")
    kpis = calculate_kpis()
    
    print("\n" + "=" * 50)
    print("KPI SUMMARY")
    print("=" * 50)
    print(f"Total Sales: ${kpis['total_sales']:,.2f}")
    print(f"Total Profit: ${kpis['total_profit']:,.2f}")
    print(f"Total Quantity Sold: {kpis['total_quantity']:,}")
    print(f"Average Discount: {kpis['avg_discount']}%")
    print(f"Profit Margin: {kpis['profit_margin']}%")
    print("=" * 50)
    
    # Step 3: Start Flask web server
    print("\nStarting Flask web server...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, port=5000)