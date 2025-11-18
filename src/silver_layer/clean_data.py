"""Takes a dataframe and returns situationally cleaned data"""
import logging
import pandas as pd
logger = logging.getLogger(__name__)

def standardize_names(df) -> pd.DataFrame:
    """Properly Capitalizes Names"""
    logger.info('Standardizing Names.')
    df['name']=df['name'].str.title()
    return df

def standardize_bill(df) -> pd.DataFrame:
    """Round bills to the nearest cent at 2 points of precision"""
    logger.info('Standardizing Bill Amount.')
    df['billing_amount'] = df['billing_amount'].round(2)
    return df

def standardize_columns(df) -> pd.DataFrame:
    """snake_case all column names"""
    logger.info('Standardizing the column names.')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')
    return df

def clean_data(df) -> pd.DataFrame:
    """Use all forms of standardization to clean the data"""
    df = standardize_names(df)
    df = standardize_bill(df)
    return df
