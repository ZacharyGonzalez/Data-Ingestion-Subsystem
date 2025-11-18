"""Sends data to the postgres container"""

import time
import logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine, text
import psycopg2

logger = logging.getLogger(__name__)


PATIENT_INSERT = """
INSERT INTO patient(name, age, gender, blood_type, medical_condition, medication, test_results)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT(patient_id) DO NOTHING
RETURNING patient_id
"""
INSURANCE_INSERT = """
INSERT INTO insurance(insurance_provider, billing_amount, patient_id)
VALUES (%s, %s, %s)
ON CONFLICT(insurance_claim) DO NOTHING
"""
ADMISSION_INSERT = """
INSERT INTO admissions(hospital, room_number, date_of_admission, discharge_date, admission_type, patient_id)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT(admission_id) DO NOTHING
"""


def get_connection():
    try:
        return psycopg2.connect(
            database="source_db",
            user="postgres",
            password="secret",
            host="source_postgres",
            port=5432,
        )
    except:
        logger.exception("Connection to DB failed")
        raise Exception


def load_data(healthcare_dataframe, retries=5, delay=3) -> None:
    """Send data to the database"""
    for i in range(retries):
        logger.info("Attempting to insert with psycopg2, attempt %s...", i)
        try:
            with get_connection() as conn, conn.cursor() as curr:
                for i, row in healthcare_dataframe.iterrows():
                    curr.execute(
                        PATIENT_INSERT,
                        (
                            row["name"],
                            row["age"],
                            row["gender"],
                            row["blood_type"],
                            row["medical_condition"],
                            row["medication"],
                            row["test_results"],
                        ),
                    )
                    patient_id = curr.fetchone()[0]
                    curr.execute(
                        INSURANCE_INSERT,
                        (row["insurance_provider"], row["billing_amount"], patient_id),
                    )
                    curr.execute(
                        ADMISSION_INSERT,
                        (
                            row["hospital"],
                            row["room_number"],
                            row["date_of_admission"],
                            row["discharge_date"],
                            row["admission_type"],
                            patient_id,
                        ),
                    )
                conn.commit()
                logger.info(
                    "Successfully wrote %s rows to Postgres.", len(healthcare_dataframe)
                )
                break
        except Exception:
            logger.warning(
                "Failed, retrying transaction in %s seconds. %s/%s retries.",
                delay,
                i,
                retries,
            )
            time.sleep(delay)
    else:
        logger.error("Failed to write to Database after %s tries.", retries)
        raise Exception("Could not connect to DB.")
