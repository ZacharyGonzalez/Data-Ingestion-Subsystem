import pandas as pd 
from src.silver_layer.clean_data import standardize_names, standardize_bill, standardize_columns
"""ok my tests fail now, whatever fix this later"""
def test_standardize_names():
    df = pd.DataFrame({
        "Name":["AlicE jane","bob", 'bob', 'JOE DIRT']
    })
    result = standardize_names(df)
    expected_names = ["Alice Jane", 'Bob', 'Bob', 'Joe Dirt']
    assert result["Name"].tolist() == expected_names
    
def test_standardize_bill():
    df = pd.DataFrame({
        "Billing Amount":[123.456,1.00,1.00,567.89652],
    })
    result = standardize_bill(df)
    expected_bills = [123.46, 1.00, 1.00, 567.90]
    assert result["Billing Amount"].tolist() == expected_bills

def test_standardize_columns():
    df = pd.DataFrame({
        "unStandaRd Columns":[1,1,1,2]
    })
    result = standardize_columns(df)
    expected_columns = ['unstandard_columns']
    assert [result.columns] == expected_columns

def test_standardize_columns_spaces(): # MULTIPLE SPACES WILL BREAK THIS STILL
    df = pd.DataFrame({
        "unStandaRd    Columns":[1,1,1,2]
    })
    result = standardize_columns(df)
    expected_columns = ['unstandard_columns']
    assert [result.columns] == expected_columns