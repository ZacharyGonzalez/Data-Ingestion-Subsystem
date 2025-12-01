"""
Main module to start the ETL Pipeline
"""

from readers.csv_reader import safe_read_csv
from silver_layer.clean_data import clean_data
from silver_layer.clean_data import standardize_columns
from silver_layer.clean_data import drop_duplicates_or_na
from silver_layer.load_data import load_data
from silver_layer.validate_data import validate_data
from logger import make_logger
CSV_PATH = "./data/output_shuffled.csv"
CHUNK_SIZE = 5000



def main():
    """Runs the primary stages of the ETL Pipeline"""
    logger = make_logger()
    reject_total = 0
    valid_total = 0
    for chunk in safe_read_csv(CSV_PATH, CHUNK_SIZE):
        chunk = standardize_columns(chunk)
        valid_df, rejects_df = validate_data(chunk)
        reject_total += len(rejects_df)
        valid_total += len(valid_df)
        clean_valid_df = clean_data(valid_df)
        if len(clean_valid_df) > 0:
            clean_valid_df = drop_duplicates_or_na(clean_valid_df)
            load_data(clean_valid_df) 
        logger.info('\n')       

if __name__ == "__main__":
    main()
