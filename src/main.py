"""
Main module to start the ETL Pipeline
"""

import logging
import os
from datetime import datetime
from readers.csv_reader import read_csv
from silver_layer.clean_data import clean_data
from silver_layer.clean_data import standardize_columns
from silver_layer.load_data import load_data
from silver_layer.drop_rows import drop_duplicates_or_na
from silver_layer.validate_data import validate_data

HEALTHCARE_CSV_PATH = "./data/healthcare_dataset.csv"


def make_logger():
    os.makedirs("./logs", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_filename = f"./logs/etl_pipeline_{now}.log"
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename=log_filename,
        filemode="w",
        encoding="utf-8",
        level=logging.INFO,
    )
    logger.info("Logger Initialization success.")


def main():
    """Runs the primary stages of the ETL Pipeline"""
    make_logger()
    df = read_csv(HEALTHCARE_CSV_PATH)
    df = standardize_columns(df)
    df, rejects = validate_data(df)
    df = drop_duplicates_or_na(df)
    df = clean_data(df)
    load_data(df)


if __name__ == "__main__":
    main()
