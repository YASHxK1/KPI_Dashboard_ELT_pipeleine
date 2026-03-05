import os
from etl import run_elt
from metrics import calculate_kpis
from web import create_app


def print_kpi_summary(kpis: dict) -> None:
    print("\n" + "=" * 50)
    print("KPI SUMMARY")
    print("=" * 50)
    print(f"Total Sales: ${kpis['total_sales']:,.2f}")
    print(f"Total Profit: ${kpis['total_profit']:,.2f}")
    print(f"Total Quantity Sold: {kpis['total_quantity']:,}")
    print(f"Average Discount: {kpis['avg_discount']}%")
    print(f"Profit Margin: {kpis['profit_margin']}%")
    print("=" * 50)


if __name__ == '__main__':
    data_path = os.getenv('DATA_PATH', 'Data/StoreSales.json')
    db_path = os.getenv('DB_PATH', 'sales_data.db')
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'

    print("=" * 50)
    print("Starting KPI Dashboard Setup...")
    print("=" * 50)

    rows = run_elt(data_path, db_path)
    print(f"Loaded {rows} rows into database")

    print("\nCalculating KPIs...")
    kpis = calculate_kpis(db_path)
    print_kpi_summary(kpis)

    app = create_app()
    print("\nStarting Flask web server...")
    print(f"Open your browser and go to: http://127.0.0.1:{port}")
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    app.run(debug=debug, port=port)
