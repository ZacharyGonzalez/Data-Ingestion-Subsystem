import pandas as pd

from src.silver_layer.clean_data import clean_data

df = pd.DataFrame({
    "Name":["AlicE jane","bob", 'bob', 'JOE DIRT'],
    "Billing Amount":[123.456,1.00,1.00,567.89652],
    "unStandaRd Columns":[None,1,1,2]
})

def test_standardization():

    df = pd.DataFrame({
        "Name":["AlicE jane","bob", 'bob', 'JOE DIRT'],
        "Billing Amount":[123.456,1.00,1.00,567.89652],
        "unStandaRd Columns":[None,1,1,2]
    })
    result = clean_data(df)
    expected_names = ["Alice Jane", 'Bob', 'Bob', 'Joe Dirt']
    expected_bills = [123.46, 1.00, 1.00, 567.90]
    expected_columns = ['name','billing_amount','unstandard_columns']
    assert result["name"].tolist() == expected_names
    assert result["billing_amount"].tolist() == expected_bills
    assert result.columns.tolist() == expected_columns