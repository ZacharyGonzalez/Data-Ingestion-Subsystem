import pytest
import psycopg2
import pandas as pd
from src.readers.csv_reader import safe_read_csv
from silver_layer.validate_data.validate_data import validate_data
from silver_layer.load_data.load_data import get_connection


# The below test fails due to docker postgres container not running
def test_psycopg2_connection():
    with get_connection() as conn, conn.cursor() as curr:
        curr.execute("SELECT 1")
        result = curr.fetchone()
        assert result[0] == 1


def test_pydantic_validators():
    pass


def test_csv_reader_bad_path():
    path = "bad_path"
    with pytest.raises(FileNotFoundError):
        list(
            safe_read_csv(path)
        )  # need to force the generator to iterate #Chatgpt assisted


def test_csv_reader_valid_path():
    path = "./test.csv"
    safe_read_csv(path)
