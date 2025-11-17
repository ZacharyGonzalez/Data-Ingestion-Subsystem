"""Sends data to the postgres container"""
import time
import os
import logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine
logger = logging.getLogger(__name__)

DB_NAME = os.getenv('DB_NAME')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_TABLE = os.getenv('DB_TABLE')


def load_data(healthcare_dataframe,retries=5,delay=3) -> None:
    """Send data to the database"""
    connection_string = f"postgresql://postgres:secret@source_postgres:5432/source_db"
    engine = None
    for i in range(retries):
        logger.info('Attempting to insert with engine, attempt %s...',i)
        try:
            engine = create_engine(connection_string)
            healthcare_dataframe.to_sql(
                name='healthcare',
                con=engine,
                if_exists='append',
                index=False
                )
            logger.info('Successfully wrote %s rows to Postgres.',{len(healthcare_dataframe)})
            break
        except:
            logger.warning('Failed, retrying in %s seconds. %s/%s retries.',delay,i,retries)
            time.sleep(delay)
    else:
        logger.error('Failed to create engine after %s tries.',retries)
        raise Exception("Could not connect to DB.")
