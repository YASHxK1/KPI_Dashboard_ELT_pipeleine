import sqlite3
import pandas as pd
from web import create_app


def test_dashboard_route_renders(tmp_path, monkeypatch):
    db_path = tmp_path / 'sales.db'
    data = pd.DataFrame(
        [
            {'Sales': 100, 'Profit': 10, 'Quantity': 2, 'Discount': 0.1, 'Category': 'Tech', 'Product Name': 'A'}
        ]
    )
    with sqlite3.connect(db_path) as conn:
        data.to_sql('sales', conn, if_exists='replace', index=False)

    monkeypatch.setenv('DB_PATH', str(db_path))
    app = create_app()
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    assert b'Sales KPI Dashboard' in response.data


def test_healthz_route():
    app = create_app()
    client = app.test_client()

    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'
