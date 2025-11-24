"""ok my tests fail now, whatever fix this later"""

import pandas as pd
from src.silver_layer.clean_data import (
    standardize_names,
    standardize_bill,
    standardize_columns,
    drop_duplicates_or_na,
)
 

def test_standardize_names():
    df = pd.DataFrame({"name": ["AliCe BRAIN", "bob ross"]})
    df = standardize_names(df)
    expected_names = ["Alice Brain", "Bob Ross"]
    assert df["name"].tolist() == expected_names


def test_standardize_bill():
    df = pd.DataFrame({"billing_amount": [100.0000000, 123.456]})
    df = standardize_bill(df)
    expected_bill = [100.00, 123.46]
    assert df["billing_amount"].tolist() == expected_bill


def test_standardize_column():
    df = pd.DataFrame(
        {"Name": ["AliCe BRAIN", "bob ross"], "BILLING_amouNT": [100, 200]}
    )
    df = standardize_columns(df)
    expected_columns = ["name", "billing_amount"]
    assert df.columns.to_list() == expected_columns


def test_duplicated_names():
    df = pd.DataFrame({"name": ["bob ross", "bob ross", "bob ross"]})
    df = drop_duplicates_or_na(df)
    expected_names = ["bob ross"]
    assert df["name"].tolist() == expected_names
