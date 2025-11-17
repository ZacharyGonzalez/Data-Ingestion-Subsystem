from readers.csv_reader import get_csv
from sqlalchemy import create_engine
import logging
import os
import time

DB_NAME = os.getenv('DB_NAME')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_TABLE = os.getenv('DB_TABLE')

HEALTHCARE_CSV_PATH = './data/healthcare_dataset.csv'

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename='./logs/etl_pipeline.log',
    filemode='w',
    encoding='utf-8',
    level=logging.INFO)
logger.info('Logger Initialization success.')
    
def read_input():
    logger.info(f'Reading healthcare data from {HEALTHCARE_CSV_PATH}.')
    healthcare_dataframe = get_csv(HEALTHCARE_CSV_PATH)
    return healthcare_dataframe
    
def clean_data(healthcare_dataframe):
    logger.info(f'Standardizing Names.')
    healthcare_dataframe['Name']=healthcare_dataframe['Name'].str.title()
    logger.info(f'Standardizing Bill Amount.')
    healthcare_dataframe['Billing Amount'] = healthcare_dataframe['Billing Amount'].round(2) 
    logger.info(f'Standardizing the column names.')
    healthcare_dataframe.columns = healthcare_dataframe.columns.str.strip().str.lower().str.replace(' ','_') 
    return healthcare_dataframe
    
def drop_duplicates_or_na(healthcare_dataframe):
    logger.info(f'Dropping duplicate entries.')
    healthcare_dataframe.drop_duplicates()
    healthcare_dataframe.dropna()
    return healthcare_dataframe

def validate_schema(df):
    return df

def load_data(healthcare_dataframe, retries=5,delay=3):
    CONNECTION_STRING = f"postgresql://postgres:secret@source_postgres:5432/source_db"
    engine = None
    for i in range(retries):   
        logger.info(f'Attempting to insert with engine, attempt {i}')
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
            logger.exception(f'Failed to create engine, retrying in {delay} seconds. {i}/{retries} retries.')
            time.sleep(delay)    
    else:
        raise Exception("Could not connect to DB")
    
def main():
    df = read_input()
    df = drop_duplicates_or_na(df)
    df = clean_data(df)
    df = validate_schema(df)
    load_data(df)
    
if __name__ == "__main__":
    main()