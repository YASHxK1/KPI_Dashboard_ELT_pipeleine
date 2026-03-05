import os
from flask import Flask, render_template
from etl import run_elt
from metrics import calculate_kpis


def create_app() -> Flask:
    app = Flask(__name__)

    data_path = os.getenv('DATA_PATH', 'Data/StoreSales.json')
    db_path = os.getenv('DB_PATH', 'sales_data.db')

    @app.route('/')
    def dashboard():
        kpis = calculate_kpis(db_path)
        return render_template('dashboard.html', kpis=kpis)

    @app.route('/healthz')
    def healthz():
        return {'status': 'ok'}, 200

    @app.cli.command('load-data')
    def load_data_command():
        rows = run_elt(data_path, db_path)
        print(f'Loaded {rows} rows into {db_path}')

    return app
