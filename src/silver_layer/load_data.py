"""Sends data to the postgres container"""
import time
import os
import logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine, text
import psycopg2
logger = logging.getLogger(__name__)


PATIENT_INSERT = """
INSERT INTO patient(name, age, gender, blood_type, medical_condition, medication, test_results)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT(patient_id) DO NOTHING
"""

def get_connection():
    try:
        return psycopg2.connect(
            database='source_db',
            user='postgres',
            password='secret',
            host="source_postgres",
            port=5432,
        )
    except:
        logger.exception("Connection to DB failed")
        raise Exception

def load_data(healthcare_dataframe,retries=5,delay=3) -> None:
    """Send data to the database"""
    connection_string = "postgresql://postgres:secret@source_postgres:5432/source_db"
    engine = None
    for i in range(retries):
        logger.info('Attempting to insert with engine, attempt %s...',i)
        try:
            with get_connection() as conn, conn.cursor() as curr:
                for i, row in healthcare_dataframe.iterrows():
                    curr.execute(
                        PATIENT_INSERT,
                        (
                            row['name'],
                            row['age'],
                            row['gender'],
                            row['blood_type'],
                            row['medical_condition'],
                            row['medication'],
                            row['test_results']
                            )
                        )
                    patient_id = curr.fetchone()[0]
                conn.commit()
                logger.info('Successfully wrote %s rows to Postgres.',len(healthcare_dataframe))
            break
        except Exception:
            logger.warning('Failed, retrying in %s seconds. %s/%s retries.',delay,i,retries)
            time.sleep(delay)
    else:
        logger.error('Failed to create engine after %s tries.',retries)
        raise Exception("Could not connect to DB.")
