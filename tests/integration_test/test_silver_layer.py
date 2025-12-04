import pandas as pd
import pytest
from silver_layer.clean_data.clean_data import clean_data


def test_clean_data_no_fail():
    df = pd.DataFrame(
        {"name": ["AliCe BRAIN", "bob ross"], "billing_amount": [100.000001, 123.456]}
    )

    df = clean_data(df)
    expected_bill = [100.00, 123.46]
    assert df["billing_amount"].tolist() == expected_bill

    expected_names = ["Alice Brain", "Bob Ross"]
    assert df["name"].tolist() == expected_names


def test_clean_data_fail():
    df = pd.DataFrame(
        {"name": ["AliCe BRAIN", 1], "billing_amount": ["100.000001", 123.456]}
    )

    with pytest.raises(TypeError):
        df = clean_data(df)
