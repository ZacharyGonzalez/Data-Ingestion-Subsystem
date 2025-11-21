"""Sends data to the postgres container

TODO Deletion of a visit should get rid of the diagnosis
"""
import time
import logging
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

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


def get_connection(retries=5, delay=3):
    load_dotenv()
    DATABASE = os.getenv("DATABASE")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    for i in range(retries):
        logger.info("Making PSYCOPG2 connection!")
        try:
            return psycopg2.connect(
                database=DATABASE,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
            )
        except:
            logger.warning("Connection to DB failed, retry %s/%s", i, retries)
            time.sleep(delay)
    logger.exception("Failed to connect to DB after %s tries.", retries)


def load_data(
    healthcare_dataframe: pd.DataFrame, rejects_dataframe: pd.DataFrame
) -> None:
    """Send data to the database"""
    with get_connection() as conn, conn.cursor() as curr:
        logger.info("Attempting to insert with psycopg2...")
        try:
            for _, row in healthcare_dataframe.iterrows():
                curr.execute(
                    PATIENT_INSERT,
                    (row["name"], row["age"], row["gender"], row["blood_type"]),
                )
                patient_id = curr.fetchone()[0]
                curr.execute(
                    CLAIM_INSERT,
                    (patient_id, row["insurance_provider"], row["billing_amount"]),
                )
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
            conn.commit()
            logger.info(
                "Successfully wrote %s rows to Postgres.", len(healthcare_dataframe)
            )
        except Exception as e:
            logger.error("Failed to write to Database")
            conn.rollback()
            raise Exception(f"Could not connect to DB for reason: {e}")
