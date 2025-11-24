import pytest
import pandas as pd
from src.readers.csv_reader import safe_read_csv
from src.silver_layer.validate_data import validate_data
# Test psycopg2 connections and terminate them
def test_psycopg2_connection():
    pass
# Test pydantic validators
def test_pydantic_validators():
    df = pd.DataFrame({
        
    })
    valid,rejects=validate_data(df)

# Test CSV Reader
def test_csv_reader_bad_path():
    path = "bad_path"
    with pytest.raises(FileNotFoundError):
        list(safe_read_csv(path)) # need to force the generator to iterate #Chatgpt assisted
        
def test_csv_reader_valid_path():
    path = "./test.csv"
    safe_read_csv(path)