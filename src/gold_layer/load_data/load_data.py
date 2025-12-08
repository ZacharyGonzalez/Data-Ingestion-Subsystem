"""Sends data to the postgres container
"""

import time
import logging
import pandas as pd
from db_connection.db_pool import get_connection
from logger import log_function_call
from .insertions.insertions import (
    claim_insertion,
    visit_insertion,
    patient_insertion,
    diagnosis_insertion,
)

logger = logging.getLogger(__name__)


@log_function_call
def load_data(healthcare_dataframe: pd.DataFrame) -> None:
    """Send data to the database"""
    with get_connection() as conn, conn.cursor() as curr:
        logger.info("Attempting to insert with psycopg2...")
        try:
            for _, row in healthcare_dataframe.iterrows():
                patient_id = patient_insertion(curr, row)
                claim_insertion(curr, row, patient_id)
                diagnosis_id = diagnosis_insertion(curr, row, patient_id)
                visit_insertion(curr, row, patient_id, diagnosis_id)
            conn.commit()
            logger.info(
                "Successfully wrote %s rows to Postgres.",
                len(
                    healthcare_dataframe
                ),  # this is wrong, we need to track updated records
            )
        except Exception as e:
            logger.error("Failed to write to Database")
            conn.rollback()
            raise Exception(f"Could not connect to DB for reason: {e}")


def load_reject_data(bad_data: pd.DataFrame) -> None:
    pass
