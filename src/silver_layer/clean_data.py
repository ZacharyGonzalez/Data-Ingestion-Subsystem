"""Takes a dataframe and returns situationally cleaned data"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def standardize_names(df) -> pd.DataFrame:
    """Properly Capitalizes Names"""
    logger.info("Standardizing Names...")
    df["name"] = df["name"].str.title()
    return df


def standardize_bill(df) -> pd.DataFrame:
    """Round bills to the nearest cent at 2 points of precision"""
    logger.info("Standardizing Bill Amount...")
    df["billing_amount"] = df["billing_amount"].round(2)
    return df


def standardize_columns(df) -> pd.DataFrame:
    """snake_case all column names"""
    logger.info("Standardizing the column names...")
    df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_")) # I should break this apart into a for loop so others can read it better
    return df


def drop_duplicates_or_na(healthcare_dataframe):
    """This function will only fail if the dataframe is None or completely empty"""
    logger.info("Dropping duplicate entries...")
    df = healthcare_dataframe.drop_duplicates() 
    df = df.dropna()
    logger.info("Successfully dropped duplicate entries.")
    return df


def clean_data(df) -> pd.DataFrame:
    """Use all forms of implemented standardization to clean the data"""
    logger.info("Attempting to clean data...")
    try:
        df = standardize_names(df)
        df = standardize_bill(df)
    except:
        logger.exception("Error on cleaning data, ensure DF is non-empty")
    return df if len(df) >= 0 else None
