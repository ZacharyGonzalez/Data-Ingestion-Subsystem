"""
Main module to start the ETL Pipeline
"""
import logging
import os
from datetime import datetime
from readers.csv_reader import read_csv
from silver_layer.clean_data import clean_data
from silver_layer.load_data import load_data
from silver_layer.drop_rows import drop_duplicates_or_na
from silver_layer.validate_data import validate_data

os.makedirs('./logs', exist_ok=True)
timestamp = datetime.now().strftime('%m%d/Y_%H%M%S')
log_filename=f'./logs/etl_pipeline_{timestamp}.log'
logger = logging.getLogger(__name__)
HEALTHCARE_CSV_PATH = './data/healthcare_dataset.csv'

logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename=log_filename,
    filemode='w',
    encoding='utf-8',
    level=logging.INFO)
logger.info('Logger Initialization success.')

def main():
    """Runs the primary stages of the ETL Pipeline
    """
    df = read_csv(HEALTHCARE_CSV_PATH)
    df = drop_duplicates_or_na(df)
    df = clean_data(df)
    df = validate_data(df)
    load_data(df)

if __name__ == "__main__":
    main()
