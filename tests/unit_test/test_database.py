import pytest
import psycopg2
import pandas as pd
from src.readers.csv_reader import safe_read_csv
from src.silver_layer.validate_data import validate_data
from src.silver_layer.load_data import get_connection

# Test psycopg2 connections and terminate them
def test_psycopg2_connection():
        conn = get_connection() 
        assert conn is not None
        try:
            curr = conn.cursor()
            curr.execute("SELECT 1")
            result = curr.fetchone()
            assert result[0] == 1
        except psycopg2.Error as e:
            assert False
        finally:
            conn.close()
        
# Test pydantic validators
def test_pydantic_validators():
    pass

# Test CSV Reader
def test_csv_reader_bad_path():
    path = "bad_path"
    with pytest.raises(FileNotFoundError):
        list(safe_read_csv(path)) # need to force the generator to iterate #Chatgpt assisted
        
def test_csv_reader_valid_path():
    path = "./test.csv"
    safe_read_csv(path)