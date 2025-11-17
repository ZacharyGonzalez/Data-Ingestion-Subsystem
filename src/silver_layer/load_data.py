from sqlalchemy import create_engine
import time
import os
from sqlalchemy.dialects.postgresql import insert
import logging
logger = logging.getLogger(__name__)

DB_NAME = os.getenv('DB_NAME')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_TABLE = os.getenv('DB_TABLE')


def load_data(healthcare_dataframe,retries=5,delay=3) -> None:
    CONNECTION_STRING = f"postgresql://postgres:secret@source_postgres:5432/source_db"
    engine = None
    for i in range(retries):   
        logger.info(f'Attempting to insert with engine, attempt {i}...')
        try:
            engine = create_engine(CONNECTION_STRING)
            healthcare_dataframe.to_sql(
                name='healthcare',
                con=engine,
                if_exists='append',
                index=False
                )
            logger.info(f'Successfully wrote {len(healthcare_dataframe)} rows to Postgres.')
            break
        except Exception as e:
            logger.warning(f'Failed to create engine, retrying in {delay} seconds. {i}/{retries} retries.')
            time.sleep(delay)    
    else:
        logger.error(f'Failed to create engine after {retries} tries.')
        raise Exception("Could not connect to DB.")
