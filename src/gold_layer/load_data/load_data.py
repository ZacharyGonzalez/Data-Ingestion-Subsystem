"""Sends data to the postgres container

TODO Deletion of a visit should get rid of the diagnosis
"""

import logging
import pandas as pd
from db_connection.db_pool import get_connection
from logger import log_function_call
from .insertions.insertions import (
    claim_insertion,
    location_insertion,
    patient_insertion,
    diagnosis_insertion,
)

logger = logging.getLogger(__name__)


@log_function_call
def load_data(healthcare_dataframe: pd.DataFrame):  # TODO add functions return type
    """Send data to the database"""
    with get_connection() as conn, conn.cursor() as curr:
        insert_count, update_count = 0, 0
        logger.info("Attempting to insert with psycopg2...")
        try:
            for _, row in healthcare_dataframe.iterrows():
                patient_id, inserted = patient_insertion(curr, row)
                if inserted:
                    insert_count += 1
                    location_insertion(curr, row, patient_id)
                    claim_insertion(curr, row, patient_id)
                    diagnosis_insertion(curr, row, patient_id)
                else:
                    update_count += 1
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
    return (insert_count, update_count)


def load_reject_data(bad_data: pd.DataFrame) -> None:
    pass
