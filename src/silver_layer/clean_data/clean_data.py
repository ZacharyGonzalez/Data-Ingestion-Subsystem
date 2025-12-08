"""Takes a dataframe and returns situationally cleaned data"""

import logging
import pandas as pd
from logger import log_function_call

logger = logging.getLogger(__name__)


@log_function_call
def standardize_names(df: pd.DataFrame) -> pd.DataFrame:
    """Properly Capitalizes Names"""
    df["name"] = df["name"].str.title()
    return df


@log_function_call
def standardize_bill(df: pd.DataFrame) -> pd.DataFrame:
    """Round bills to the nearest cent at 2 points of precision"""
    df["billing_amount"] = df["billing_amount"].round(2)
    return df


@log_function_call
def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """snake_case all column names"""
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    return df


@log_function_call
def drop_duplicates_or_na(healthcare_dataframe: pd.DataFrame) -> pd.DataFrame:
    """This function will only fail if the dataframe is None or completely empty"""
    df = healthcare_dataframe.drop_duplicates()
    num_duplicates = df.duplicated().sum()
    logger.info("removed %s duplicates from current chunk", num_duplicates)
    df = df.dropna()
    return df


@log_function_call # i hate this function
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Use all forms of implemented standardization to clean the data"""
    try:
        df = standardize_names(df)
    except TypeError as e:
        logger.exception("Error on standardizing names %s", e)
        raise e

    try:
        df = standardize_bill(df)
    except TypeError as e:
        logger.exception("Error on standardizing bills %s", e)
        # Willing to continue on bad clean since the validator will handle the rest
    return df
