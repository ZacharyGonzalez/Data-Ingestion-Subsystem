import logging
logger = logging.getLogger(__name__)

def drop_duplicates_or_na(healthcare_dataframe):
    logger.info(f'Dropping duplicate entries.')
    healthcare_dataframe.drop_duplicates()
    healthcare_dataframe.dropna()
    logger.info(f'Successfully dropped duplicate entries.')
    return healthcare_dataframe
