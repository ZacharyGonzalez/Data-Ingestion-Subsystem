"""
Main module to start the ETL Pipeline
"""

from bronze_layer.csv_reader import safe_read_csv
from gold_layer.load_data.load_data import load_data
from silver_layer.validate_data.validate_data import validate_data
from logger import make_logger
from silver_layer.clean_data.clean_data import (
    clean_data,
    drop_duplicates_or_na,
    standardize_columns,
)
from gold_layer.analytics.queries import (
    top_conditions,
    avg_billing_by_insurance,
    patient_count_by_gender,
)

CSV_PATH = "./data/output_shuffled.csv"
CHUNK_SIZE = 5000


def main():
    """Runs the primary stages of the ETL Pipeline.

    We clean the data before checking for duplicates because unstandardized names are not equal to eachother even if they are the same spelling.
    Duplicates from chunk are checked due to its speed, but duplicate patients will be caught and handled by postgres.
    """

    logger = make_logger()
    for chunk in safe_read_csv(CSV_PATH, CHUNK_SIZE):
        chunk = standardize_columns(chunk)
        clean_df = clean_data(chunk)
        valid_df, rejects_df = validate_data(clean_df)
        if len(valid_df) > 0:
            valid_df = drop_duplicates_or_na(valid_df)
            load_data(valid_df)
    logger.info("\n")
    """
    logger.info("Top diagnoses:\n%s", top_conditions())
    logger.info("Average billing by provider:\n%s", avg_billing_by_insurance())
    logger.info("Patient demographics:\n%s", patient_count_by_gender())
    """

if __name__ == "__main__":
    main()
