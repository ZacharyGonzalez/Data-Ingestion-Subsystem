import pandas as pd
import logging
logger = logging.getLogger(__name__)

def standardize_names(df) -> pd.DataFrame: 
    logger.info(f'Standardizing Names.')
    df['Name']=df['Name'].str.title()
    return df
    
    
def standardize_bill(df) -> pd.DataFrame:
    logger.info(f'Standardizing Bill Amount.')
    df['Billing Amount'] = df['Billing Amount'].round(2) 
    return df
   
   
def standardize_columns(df) -> pd.DataFrame:
    logger.info(f'Standardizing the column names.')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')  
    return df


def clean_data(df) -> pd.DataFrame:
    df = standardize_names(df)
    df = standardize_bill(df)
    df = standardize_columns(df)
    return df
    