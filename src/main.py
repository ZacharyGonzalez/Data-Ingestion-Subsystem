"""
Main module to start the ETL Pipeline
"""

import logging
import os
import time
from datetime import datetime
from readers.csv_reader import safe_read_csv
from silver_layer.clean_data import clean_data
from silver_layer.clean_data import standardize_columns
from silver_layer.clean_data import drop_duplicates_or_na
from silver_layer.load_data import load_data
from silver_layer.validate_data import validate_data

HEALTHCARE_CSV_PATH = "./data/healthcare_dataset.csv"
CHUNK_SIZE = 5000

def make_logger():
    os.environ["TZ"] = "America/New_York"
    os.makedirs("./logs", exist_ok=True)
    time.tzset()
    FILE_MODE="w"
    now = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"./logs/etl_{now}.log"
    if os.path.exists(log_filename):
        FILE_MODE = "a"
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename=log_filename,
        filemode=FILE_MODE,
        encoding="utf-8",
        level=logging.INFO,
    )
    logger.info("Logger Initialization success.")


def main():
    """Runs the primary stages of the ETL Pipeline"""
    make_logger()
    reject_total = 0
    valid_total = 0
    for chunk in safe_read_csv(HEALTHCARE_CSV_PATH, CHUNK_SIZE):
        chunk = standardize_columns(chunk)
        valid_df, rejects_df = validate_data(chunk)
        reject_total += len(rejects_df)
        valid_total += len(valid_df)
        clean_valid_df = clean_data(valid_df) # if DF is empty this will gracefully fail
        if len(clean_valid_df)>0:
            clean_valid_df = drop_duplicates_or_na(clean_valid_df)
            load_data(clean_valid_df, rejects_df)


if __name__ == "__main__":
    main()
