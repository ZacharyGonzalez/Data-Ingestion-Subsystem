"""Sends data to the postgres container"""

import time
import logging
import psycopg2
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

MEDICAL_INSERT = """
    INSERT INTO medical_record(patient_id,blood_type, medical_condition, medication, test_results)
    values (%s, %s, %s, %s, %s)
    """
PATIENT_INSERT = """
    INSERT INTO patient(name, age, gender)
    VALUES (%s, %s, %s)
    RETURNING patient_id
    """
INSURANCE_INSERT = """
    INSERT INTO insurance(insurance_provider, billing_amount, patient_id)
    VALUES (%s, %s, %s)
    """
ADMISSION_INSERT = """
    INSERT INTO admissions(hospital, room_number, date_of_admission, discharge_date, admission_type, patient_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING admission_id
    """


def get_connection(retries=5, delay=3):
    load_dotenv()
    DATABASE = os.getenv("DATABASE")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    for i in range(retries):
        logger.info('Making PSYCOPG2 connection!')
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


def load_data(healthcare_dataframe) -> None:
    """Send data to the database"""
    with get_connection() as conn, conn.cursor() as curr:
        logger.info("Attempting to insert with psycopg2...")
        try:
            for _, row in healthcare_dataframe.iterrows():
                curr.execute(
                    PATIENT_INSERT,
                    (
                        row["name"],
                        row["age"],
                        row["gender"],
                    ),
                )
                patient_id = curr.fetchone()[0]
                curr.execute(
                    MEDICAL_INSERT,
                    (
                        patient_id,
                        row["blood_type"],
                        row["medical_condition"],
                        row["medication"],
                        row["test_results"],
                    ),
                )
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
                admission_id = curr.fetchone()[0]
            conn.commit()
            logger.info(
                "Successfully wrote %s rows to Postgres.", len(healthcare_dataframe)
            )
        except Exception as e:
            logger.error("Failed to write to Database")
            conn.rollback()
            raise Exception(f"Could not connect to DB for reason: {e}")
