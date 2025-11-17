from readers.csv_reader import get_csv
from sqlalchemy import create_engine
import logging
import os

DB_NAME = os.getenv('PGDB')
DB_PASS = os.getenv('PGPASS')
DB_HOST = os.getenv('PGHOST')
DB_PORT = os.getenv('DBPORT')

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename='./logs/etl_pipeline.log',
    filemode='w',
    encoding='utf-8',
    level=logging.INFO)
logger.info('Logger Initialization success.')

HEALTHCARE_CSV_PATH = './data/healthcare_dataset.csv'
healthcare_dataframe = get_csv(HEALTHCARE_CSV_PATH)

healthcare_dataframe.drop_duplicates()
healthcare_dataframe.dropna()
healthcare_dataframe['Name']=healthcare_dataframe['Name'].str.title()
healthcare_dataframe['Billing Amount'] = healthcare_dataframe['Billing Amount'].round(2) 
healthcare_dataframe.columns = healthcare_dataframe.columns.str.strip().str.lower().str.replace(' ','_') 

CONNECTION_STRING = "postgresql://{DB_HOST}:{DB_PASS}@source_postgres:{DB_PORT}/{DB_NAME}"

logger.info(f'Attempting to insert with engine')
try:
    engine = create_engine(CONNECTION_STRING)
    subset_df = healthcare_dataframe.head(5)
    subset_df.to_sql(
        name='healthcare',
        con=engine,
        if_exists='append',
        index=False
        )
    logger.info(f'Successfully wrote {len(subset_df)} rows to Postgres.')
except Exception as e:
    logger.exception(f'Failed to create engine')