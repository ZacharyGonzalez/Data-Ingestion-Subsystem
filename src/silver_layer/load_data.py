"""Sends data to the postgres container

TODO Deletion of a visit should get rid of the diagnosis
"""

import time
import logging
import pandas as pd
from .db_pool import get_connection
from logger import log_function_call

logger = logging.getLogger(__name__)

DIAGNOSIS_INSERT = """
    INSERT INTO diagnosis(patient_id,  doctor,  medical_condition, medication, test_results)
    values (%s, %s, %s, %s, %s)
    RETURNING diagnosis_id
    """
PATIENT_INSERT = """
    INSERT INTO patient(name, age, gender, blood_type)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (name, age, gender, blood_type) 
    DO UPDATE SET name = EXCLUDED.name
    RETURNING patient_id
    """
CLAIM_INSERT = """
    INSERT INTO claim(patient_id, insurance_provider, billing_amount)
    VALUES (%s, %s, %s)
    """
VISIT_INSERT = """
    INSERT INTO visit(patient_id, diagnosis_id, hospital, room_number, date_of_admission, discharge_date, admission_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """


def patient_insertion(curr, row):
    curr.execute(
        PATIENT_INSERT,
        (row["name"], row["age"], row["gender"], row["blood_type"]),
    )
    patient_id = curr.fetchone()[0]
    return patient_id


def claim_insertion(curr, row, patient_id):
    curr.execute(
        CLAIM_INSERT,
        (patient_id, row["insurance_provider"], row["billing_amount"]),
    )


def diagnosis_insertion(curr, row, patient_id):
    curr.execute(
        DIAGNOSIS_INSERT,
        (
            patient_id,
            row["doctor"],
            row["medical_condition"],
            row["medication"],
            row["test_results"],
        ),
    )
    diagnosis_id = curr.fetchone()[0]
    return diagnosis_id


def visit_insertion(curr, row, patient_id, diagnosis_id):
    curr.execute(
        VISIT_INSERT,
        (
            patient_id,
            diagnosis_id,
            row["hospital"],
            row["room_number"],
            row["date_of_admission"],
            row["discharge_date"],
            row["admission_type"],
        ),
    )

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
