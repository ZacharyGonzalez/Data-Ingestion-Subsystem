"""
Main module to start the ETL Pipeline
"""

from readers.csv_reader import safe_read_csv
from silver_layer.load_data.load_data import load_data
from silver_layer.validate_data.validate_data import validate_data
from logger import make_logger
from silver_layer.clean_data.clean_data import (
    clean_data,
    drop_duplicates_or_na,
    standardize_columns,
)

CSV_PATH = "./data/output_shuffled.csv"
CHUNK_SIZE = 5000


def main():
    """Runs the primary stages of the ETL Pipeline.
    
    We clean the data before checking for duplicates because unstandardized names are not equal to eachother even if they are the same spelling
    """
    logger = make_logger()
    for chunk in safe_read_csv(CSV_PATH, CHUNK_SIZE):
        chunk = standardize_columns(chunk)
        valid_df, rejects_df = validate_data(chunk)
        clean_valid_df = clean_data(valid_df)
        if len(clean_valid_df) > 0:
            clean_valid_df = drop_duplicates_or_na(clean_valid_df)
            load_data(clean_valid_df)
        logger.info("\n")


if __name__ == "__main__":
    main()
