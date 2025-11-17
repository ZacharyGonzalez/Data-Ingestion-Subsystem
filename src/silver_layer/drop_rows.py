"""This module drops duplicates and None fields"""
import logging
logger = logging.getLogger(__name__)

def drop_duplicates_or_na(healthcare_dataframe):
    """This function will only fail if the dataframe is None or completely empty"""
    logger.info('Dropping duplicate entries.')
    healthcare_dataframe.drop_duplicates()
    healthcare_dataframe.dropna()
    logger.info('Successfully dropped duplicate entries.')
    return healthcare_dataframe
