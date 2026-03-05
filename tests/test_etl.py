import json
import pytest
from etl import extract_data, transform_data


def test_extract_data_requires_columns(tmp_path):
    p = tmp_path / 'bad.json'
    p.write_text(json.dumps([{'Sales': 10}]), encoding='utf-8')

    with pytest.raises(ValueError):
        extract_data(str(p))


def test_transform_data_cleans_numeric_values():
    import pandas as pd

    df = pd.DataFrame(
        [
            {
                'Sales': '100.5',
                'Profit': 'bad',
                'Quantity': '2',
                'Discount': None,
                'Category': 'Tech',
                'Product Name': 'A',
            }
        ]
    )

    out = transform_data(df)
    assert out.loc[0, 'Sales'] == 100.5
    assert out.loc[0, 'Profit'] == 0
    assert out.loc[0, 'Quantity'] == 2
    assert out.loc[0, 'Discount'] == 0
